FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base

WORKDIR /app

COPY API/*.csproj API/
COPY Core/*.csproj Core/
COPY Infrastructure/*.csproj Infrastructure/

RUN dotnet restore API/API.csproj

COPY . .

EXPOSE 5000
EXPOSE 5001

ENTRYPOINT [ "dotnet", "watch", "--project", "API/API.csproj", "run", "--urls", "http://0.0.0.0:5001" ]