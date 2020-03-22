# Dasiado
Bot no telegram para gerenciamento das chaves da salinha

Hospedado no Heroku do Dasi USP, token no BitWarden

# Deploy:
gcloud beta functions deploy webhook --set-env-vars "TELEGRAM_TOKEN=[SECRET]" --runtime python37 --trigger-http
Na GCloud do DASI

Token está no BitWarden do Diretor de T.I.
