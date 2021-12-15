import math

import torch
from transformers import GPT2Config
from transformers import GPT2PreTrainedModel



def gelu(x):
    srqt_2_pi = 0.7978845608
    return .5 * x * (1 + torch.tanh(srqt_2_pi * (x + .044715 * (x ** 3))))


class Conv1D(torch.nn.Module):
    def __init__(self, nf, nx):
        """ Conv1D layer as defined by Radford et al. for OpenAI GPT (and also used in GPT-2)
            Basically works like a Linear layer but the weights are transposed
        """
        super(Conv1D, self).__init__()
        self.nf = nf
        w = torch.empty(nx, nf)
        torch.nn.init.normal_(w, std=0.02)
        self.weight = torch.nn.Parameter(w)
        self._weightT = None
        self.bias = torch.nn.Parameter(torch.zeros(nf))

    def forward(self, x):
        if self._weightT is None:
            self._weightT = self.weight.T
        return torch.nn.functional.linear(x, self._weightT, self.bias)


class Attention(torch.nn.Module):
    def __init__(self, n_embd, n_ctx, config):
        super(Attention, self).__init__()
        # in Attention: n_embd=768 (nx=n_embd)
        # [switch nx => n_embd from Block to Attention to keep identical to TF implem]
        assert n_embd % config.n_head == 0
        self.register_buffer("m1e4", torch.full((1, 1, 1), -1e4))
        self.n_head = config.n_head
        self.n_embd = n_embd

        self.c_attn = Conv1D(n_embd * 3, n_embd)
        self.c_proj = Conv1D(n_embd, n_embd)

    def _attn(self, q, k, v, mask):
        w = torch.matmul(q, k)
        w /= math.sqrt(v.size(-1))

        w = torch.where(mask, w, self.m1e4)
        w = torch.nn.Softmax(dim=-1)(w)
        return torch.matmul(w, v)

    def merge_heads(self, x: torch.Tensor):
        x = x.permute(1, 0, 2).contiguous()
        new_x_shape = x.size()[:-2] + (self.n_embd,)
        return x.view(*new_x_shape)  # in Tensorflow implem: fct merge_states

    def split_heads(self, x):
        new_x_shape = x.size()[:-1] + (self.n_head, self.n_embd // self.n_head)
        x = x.view(*new_x_shape)  # in Tensorflow implem: fct split_states
        return x.permute(1, 0, 2)  # (batch, head, seq_length, head_features)

    def forward(self, x, layer_past, mask):
        x = self.c_attn(x)
        x = x.view((x.size(0), 3, self.n_embd))
        query, key, value = x[:, 0], x[:, 1], x[:, 2]
        # query, key, value = x.split(self.n_embd, dim=2)
        query = self.split_heads(query)
        key = self.split_heads(key)  # , k=True)
        value = self.split_heads(value)

        if layer_past is not None:
            past_value = layer_past[1]  # transpose back cf below
            value = torch.cat((past_value, value), dim=-2)

            past_key = layer_past[0]  # .transpose(-2, -1)
            key = torch.cat((past_key, key), dim=-2)

        present = torch.stack([key, value])  # transpose to have same shapes for stacking

        a = self._attn(query, key.transpose(-2, -1), value, mask)
        a = self.merge_heads(a)
        a = self.c_proj(a)

        return a, present


class MLP(torch.nn.Module):
    def __init__(self, n_state, config):  # in MLP: n_state=3072 (4 * n_embd)
        super(MLP, self).__init__()
        self.c_fc = Conv1D(n_state, config.n_embd)
        self.c_proj = Conv1D(config.n_embd, n_state)
        if hasattr(torch.nn, 'GELU'):
            self.act = torch.nn.GELU()  # New in torch 1.4.0, but different results from transformers gelu
        else:
            self.act = gelu  # the original gelu, written in pytorch

    def forward(self, x):
        h = self.act(self.c_fc(x))
        h2 = self.c_proj(h)
        return h2


class Block(torch.nn.Module):
    def __init__(self, n_ctx, config):
        super(Block, self).__init__()
        n_embd = config.n_embd
        self.ln_1 = torch.nn.LayerNorm(n_embd, eps=config.layer_norm_epsilon)
        self.attn = Attention(n_embd, n_ctx, config)
        self.ln_2 = torch.nn.LayerNorm(n_embd, eps=config.layer_norm_epsilon)
        self.mlp = MLP(4 * n_embd, config)

    def forward(self, x, layer_past, mask):
        a, present = self.attn(self.ln_1(x), layer_past, mask)
        x = x + a
        x += self.mlp(self.ln_2(x))  # residual

        return x, present  # x, present


class GPT2Model(GPT2PreTrainedModel):

    def __init__(self, config: GPT2Config):
        super(GPT2Model, self).__init__(config)

        self.wte = torch.nn.Embedding(config.vocab_size, config.n_embd)
        self.wpe = torch.nn.Embedding(config.n_positions, config.n_embd)
        self.h = torch.nn.ModuleList([Block(config.n_ctx, config) for _ in range(config.n_layer)])
        self.ln_f = torch.nn.LayerNorm(config.n_embd, eps=config.layer_norm_epsilon)
        self.register_buffer("bigmask", torch.tril(torch.ones((config.n_ctx, config.n_ctx), dtype=torch.uint8)))
        self.init_weights()

    def get_input_embeddings(self):
        return self.wte

    def set_input_embeddings(self, new_embeddings):
        self.wte = new_embeddings

    def forward(self, input_ids: torch.Tensor, past: torch.Tensor):
        if input_ids is None:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        input_len = input_ids.size(0)
        past_length = past.size(-2) if past is not None else 0
        total_len = input_len + past_length
        position_embeds = self.wpe.weight.data[past_length:total_len]

        inputs_embeds = self.wte(input_ids)
        hidden_states = inputs_embeds + position_embeds

        mask = self.bigmask[None, past_length:total_len, :total_len]
        presents = []
        for i in range(self.config.n_layer):
            layer_past = past[i] if past is not None else None
            trans_block = self.h[i]
            hidden_states, present = trans_block(hidden_states, layer_past, mask)
            presents.append(present)

        hidden_states = self.ln_f(hidden_states)
        return hidden_states, torch.stack(presents)


class GPT2LMHeadModelExperimental(GPT2PreTrainedModel):

    def __init__(self, config):
        super(GPT2LMHeadModelExperimental, self).__init__(config)
        self.transformer = GPT2Model(config)
        self.lm_head = torch.nn.Linear(config.n_embd, config.vocab_size, bias=False)

        self.init_weights()
        self.tie_weights()

    def tie_weights(self):
        """ Make sure we are sharing the input and output embeddings.
            Export to TorchScript can't handle parameter sharing so we are cloning them instead.
        """
        self._tie_or_clone_weights(self.lm_head,
                                   self.transformer.wte)

    def forward(self, input_ids: torch.Tensor, **kwargs):
        hidden_states, pasts = self.transformer(input_ids, **kwargs)
        lm_logits = self.lm_head(hidden_states)
        return lm_logits, pasts
