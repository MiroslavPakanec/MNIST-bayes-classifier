@echo off

REM Create Docker network
docker network create --driver bridge --opt com.docker.network.bridge.name=bayes-classifier-network bayes-classifier-network

REM Navigate to the client directory and run the batch script
cd client
call restart_windows.bat

REM Navigate back to the root directory
cd ..

REM Navigate to the service directory and run the batch script
cd service
call restart_windows.bat

REM Navigate back to the root directory
cd ..