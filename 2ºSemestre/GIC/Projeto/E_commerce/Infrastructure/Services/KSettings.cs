public class KSettings
{
    public readonly string tokenKey;
    public readonly string tokenIssuer;
    public readonly string apiUrl;
    public readonly string seedDataPath;

    public KSettings()
    {
        tokenKey = GetTokenKeyString();
        tokenIssuer = GetTokenIssuerString();
        apiUrl = GetApiUrl();
        seedDataPath = GetSeedDataPath();
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

    private static string GetSeedDataPath()
    {
        var seedDataPath = Environment.GetEnvironmentVariable("SEED_DATA_PATH");
        if (string.IsNullOrEmpty(seedDataPath))
        {
            throw new Exception("Seed data path is not set in the environment variables.");
        }

        return seedDataPath;
    }
}