using System.Text;
using Core.Entities.Identity;
using Infrastructure.Data.Identity;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Pomelo.EntityFrameworkCore.MySql.Infrastructure;

namespace API.Extensions
{
    public static class IdentityServiceExtensions
    {
        public static IServiceCollection AddIdentityServices(this IServiceCollection services, Settings settings)
        {
            services.AddDbContext<AppIdentityDbContext>(opt =>
            {
                opt.UseMySql(settings.connectionString,
                    ServerVersion.AutoDetect(settings.connectionString),
                    b => b.MigrationsAssembly("Infrastructure")); // Ensure migrations are in Infrastructure
            });
            services.AddIdentityCore<AppUser>(opt =>
            {
                // add identity options here
            })
            .AddEntityFrameworkStores<AppIdentityDbContext>()
            .AddSignInManager<SignInManager<AppUser>>();

            services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
                .AddJwtBearer(options =>
                {
                    options.TokenValidationParameters = new TokenValidationParameters
                    {
                        ValidateIssuerSigningKey = true,
                        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(settings.tokenKey)),
                        ValidIssuer = settings.tokenIssuer,
                        ValidateIssuer = true,
                        ValidateAudience = false
                    };
                });


            services.AddAuthorization();

            return services;
        }
    }
}