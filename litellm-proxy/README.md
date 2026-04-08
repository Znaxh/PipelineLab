# PipelineLab — local LiteLLM proxy

Runs a small [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/docker_quick_start) so PipelineLab can use `LITELLM_BASE_URL` + `LITELLM_API_KEY` instead of calling OpenAI/Cohere directly.

## Setup (once)

```bash
cd litellm-proxy
uv venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv sync
cp .env.example .env
```

Edit `.env`:

- Set **`LITELLM_MASTER_KEY`** to a long random string (this is the “API key” PipelineLab uses).
- Set **`OPENAI_API_KEY`** and/or **`COHERE_API_KEY`** so the models in `config.yaml` can reach a provider.

## Run the proxy

Use the helper script so **`DATABASE_URL` from PipelineLab (or your shell) does not force Prisma**:

```bash
cd litellm-proxy
./run-proxy.sh
# optional: PORT=4001 ./run-proxy.sh
```

Or manually (must unset DB vars if they are set globally):

```bash
cd litellm-proxy
source .venv/bin/activate
unset DATABASE_URL DIRECT_URL DATABASE_HOST DATABASE_USERNAME DATABASE_PASSWORD DATABASE_NAME
set -a && source .env && set +a
litellm --config config.yaml --port 4000
```

Open [http://localhost:4000](http://localhost:4000) — you should see the proxy UI / health depending on version.

## PipelineLab `.env` (repo root)

Match the proxy:

```env
LITELLM_BASE_URL=http://localhost:4000
LITELLM_API_KEY=<same value as LITELLM_MASTER_KEY>
```

If the backend runs **inside Docker**, use `http://host.docker.internal:4000` (Mac/Windows) or your host IP instead of `localhost`.

## Change models

Edit `config.yaml` `model_list`, then restart the proxy.
