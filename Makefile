wg-create:
	rm -f gateway.conf
	FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) fly wireguard create personal fra gateway gateway.conf

wg-list:
	FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) fly wireguard list

gateway:
	docker compose up --build gateway

fly-deploy:
	FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) fly deploy --app inndex-jan-czechowski-com


wg-remove-all:
	@export FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) && \
	org=$$(fly status -j | jq -r '.Organization.Slug') && \
	for name in $$(fly wireguard list -j | jq -r '.[].Name'); do \
		fly wireguard remove $$org $$name; \
	done

CONFIG_FILES = Dockerfile Dockerfile.gateway fly.toml docker-compose.yml Makefile nginx-gateway.conf entrypoint.gateway.sh

copy-config:
	@( for f in $(CONFIG_FILES); do \
		echo "===== $$f ====="; \
		cat $$f; \
		echo; \
	done ) | ( base64 | tr -d '\n' | xargs -0 printf '\033]52;c;%s\a' )
