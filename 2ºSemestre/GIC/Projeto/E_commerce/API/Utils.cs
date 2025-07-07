public class Settings
{
    public readonly string connectionString;
    public readonly string cacheConnectionString;
    public readonly string tokenKey;
    public readonly string tokenIssuer;
    public readonly string apiUrl;
    public readonly string allowedHost;
    public readonly string cdnUrl;

    public Settings()
    {
        connectionString = GetMainDBConnectionString();
        cacheConnectionString = GetCacheDatabaseConnectionString();
        tokenKey = GetTokenKeyString();
        tokenIssuer = GetTokenIssuerString();
        apiUrl = GetApiUrl();
        allowedHost = GetAllowedHost();
        cdnUrl = GetCdnUrl();
    }

    private static string GetMainDBConnectionString()
    {
        var dbHost = Environment.GetEnvironmentVariable("MYSQL_HOST");
        var dbPort = Environment.GetEnvironmentVariable("MYSQL_PORT");
        var dbName = Environment.GetEnvironmentVariable("MYSQL_DATABASE");
        var dbUser = Environment.GetEnvironmentVariable("MYSQL_USER");
        var dbPassword = Environment.GetEnvironmentVariable("MYSQL_PASSWORD");

        if (string.IsNullOrEmpty(dbHost) || string.IsNullOrEmpty(dbPort) || string.IsNullOrEmpty(dbName) ||
            string.IsNullOrEmpty(dbUser) || string.IsNullOrEmpty(dbPassword))
        {
            throw new Exception("Database connection string is not set in the environment variables.");
        }

        if (!int.TryParse(dbPort, out int port))
        {
            throw new Exception("Database port is not a valid integer.");
        }

        return $"Server={dbHost};Port={dbPort};Database={dbName};User={dbUser};Password={dbPassword};";
    }

    private static string GetCacheDatabaseConnectionString()
    {
        var cacheHost = Environment.GetEnvironmentVariable("CACHE_HOST");
        var cachePort = Environment.GetEnvironmentVariable("CACHE_PORT");

        if (string.IsNullOrEmpty(cacheHost) || string.IsNullOrEmpty(cachePort))
        {
            throw new Exception("Cache connection string is not set in the environment variables.");
        }

        if (!int.TryParse(cachePort, out int port))
        {
            throw new Exception("Cache port is not a valid integer.");
        }
        
        return $"{cacheHost}:{cachePort}";
    }

    private static string GetTokenKeyString()
    {
        var tokenKey = Environment.GetEnvironmentVariable("TOKEN_SECRET_KEY");
        if (string.IsNullOrEmpty(tokenKey))
        {
            throw new Exception("Token key is not set in the environment variables.");
        }

        return tokenKey;
    }

    private static string GetTokenIssuerString()
    {
        var tokenIssuer = Environment.GetEnvironmentVariable("TOKEN_ISSUER");
        if (string.IsNullOrEmpty(tokenIssuer))
        {
            throw new Exception("Token issuer is not set in the environment variables.");
        }

        return tokenIssuer;
    }

    private static string GetApiUrl()
    {
        var apiUrl = Environment.GetEnvironmentVariable("API_URL");
        if (string.IsNullOrEmpty(apiUrl))
        {
            throw new Exception("API URL is not set in the environment variables.");
        }

        return apiUrl;
    }

    private static string GetAllowedHost()
    {
        var allowedHost = Environment.GetEnvironmentVariable("ALLOWED_HOST");
        if (string.IsNullOrEmpty(allowedHost))
        {
            throw new Exception("Allowed host is not set in the environment variables.");
        }

        return allowedHost;
    }

    private static string GetCdnUrl()
    {
        var cdnUrl = Environment.GetEnvironmentVariable("CDN_URL");
        if (string.IsNullOrEmpty(cdnUrl))
        {
            throw new Exception("CDN URL is not set in the environment variables.");
        }

        return cdnUrl;
    }
}