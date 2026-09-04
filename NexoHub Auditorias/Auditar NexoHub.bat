@echo off
chcp 65001 >nul
title NexoHub Auditorias - conteudo PUBLICADO (DeepSeek)
cd /d "%~dp0"

if not exist "chave_deepseek.txt" (
  echo.
  echo   Falta o arquivo chave_deepseek.txt nesta pasta.
  echo   Crie um arquivo de texto com a chave da API DeepSeek numa linha so.
  echo.
  pause
  exit /b 1
)
set /p DS_KEY=<chave_deepseek.txt

rem Uma credencial da Anthropic no ambiente venceria o token do DeepSeek.
set "ANTHROPIC_API_KEY="
set "ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic"
set "ANTHROPIC_AUTH_TOKEN=%DS_KEY%"
set "ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro"
set "ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro"
set "ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash"
set "CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash"
set "AUDITAR_ALVO=nexohub"

echo.
echo   Conferindo quem vai responder...
call :checar
set "DS_KEY="
echo.

claude
goto :eof

:checar
rem Pergunta ao endpoint qual modelo ele e. Se nao voltar deepseek, algo esta errado.
curl -s -m 45 "%ANTHROPIC_BASE_URL%/v1/messages" ^
  -H "content-type: application/json" ^
  -H "x-api-key: %ANTHROPIC_AUTH_TOKEN%" ^
  -H "anthropic-version: 2023-06-01" ^
  -d "{\"model\":\"%ANTHROPIC_DEFAULT_OPUS_MODEL%\",\"max_tokens\":16,\"messages\":[{\"role\":\"user\",\"content\":\"ok\"}]}" > "%TEMP%\ds_check.json" 2>nul
findstr /C:"deepseek" "%TEMP%\ds_check.json" >nul 2>&1
if errorlevel 1 (
  echo   [ATENCAO] o endpoint nao respondeu como DeepSeek.
  echo             Verifique a chave em chave_deepseek.txt.
  type "%TEMP%\ds_check.json" 2>nul
) else (
  echo   OK - respondendo como %ANTHROPIC_DEFAULT_OPUS_MODEL% via api.deepseek.com
  echo        Confirme dentro da sessao com /status
)
del "%TEMP%\ds_check.json" >nul 2>&1
exit /b
