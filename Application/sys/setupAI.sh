export STORAGE_LOCATION=$HOME/anythingllm 
if [ ! -d "$STORAGE_LOCATION" ]; then
    mkdir -p $STORAGE_LOCATION
fi
touch "$STORAGE_LOCATION/.env"
sudo docker run -d -p 3001:3001 \
--cap-add SYS_ADMIN \
-v ${STORAGE_LOCATION}:/app/server/storage \
-v ${STORAGE_LOCATION}/.env:/app/server/.env \
-e STORAGE_DIR="/app/server/storage" \
--add-host=host.docker.internal:host-gateway \
mintplexlabs/anythingllm
