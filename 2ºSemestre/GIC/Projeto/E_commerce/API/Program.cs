using API.Extensions;
using API.Middleware;
using Infrastructure.Data;
using Core.Entities.Identity;
using Infrastructure.Data.Identity;
using Infrastructure.Identity;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using HealthChecks.UI.Client;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;
using OpenTelemetry.Exporter;
using OpenTelemetry.Metrics;


var builder = WebApplication.CreateBuilder(args);
var settings = new Settings();

builder.Services.AddControllers();
builder.Services.AddApplicationServices(settings);
builder.Services.AddIdentityServices(settings);
builder.Services.AddSwaggerDocumentation();

// Health checks
builder.Services.AddHealthChecks()
    .AddMySql(settings.connectionString, name: "mysql", timeout: TimeSpan.FromSeconds(5))
    .AddRedis(settings.cacheConnectionString, name: "redis", timeout:TimeSpan.FromSeconds(5));

builder.Services.AddDbContext<StoreContext>(options =>
    options.UseMySql(settings.connectionString, new MySqlServerVersion(new Version(8, 0, 32))));
builder.Services.AddSingleton<Settings>();

builder.Services.AddOpenTelemetry()
    .WithTracing(builder => builder
        .SetResourceBuilder(
            ResourceBuilder.CreateDefault()
                .AddService(serviceName:"backend-service", serviceVersion: "1.0.0")
        )
        .AddSource("ByteBazaar API")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddSqlClientInstrumentation(options => options.SetDbStatementForText = true)
        .AddRedisInstrumentation()
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://otel-collector:4317");
            options.Protocol = OtlpExportProtocol.Grpc;
        }))
    .WithMetrics(builder => builder
        .SetResourceBuilder(
            ResourceBuilder.CreateDefault()
                .AddService(serviceName: "backend-service", serviceVersion: "1.0.0"))
        .AddAspNetCoreInstrumentation()
        .AddRuntimeInstrumentation()
        .AddHttpClientInstrumentation()
        .AddProcessInstrumentation()
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://otel-collector:4317");
            options.Protocol = OtlpExportProtocol.Grpc;
        })
);

var app = builder.Build();

// Configure the HTTP request pipeline.
app.UseMiddleware<ExceptionMiddleware>();

app.UseStatusCodePagesWithReExecute("/errors/{0}");

app.UseSwaggerDocumentation();

app.UseStaticFiles();

app.UseCors("CorsPolicy");

app.UseAuthentication();
app.UseAuthorization();

// Map health check
app.MapHealthChecks("/health", new HealthCheckOptions
{
    Predicate = _ => true,
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

app.MapControllers();

using var scope = app.Services.CreateScope();
var services = scope.ServiceProvider;
var context = services.GetRequiredService<StoreContext>();
var identityContext = services.GetRequiredService<AppIdentityDbContext>();
var userManager = services.GetRequiredService<UserManager<AppUser>>();
var logger = services.GetRequiredService<ILogger<Program>>();
try
{
    await context.Database.MigrateAsync();
    await identityContext.Database.MigrateAsync();
    await StoreContextSeed.SeedAsync(context);
    await AppIdentityDbContextSeed.SeedUsersAsync(userManager);
}
catch (Exception ex)
{
   logger.LogError(ex, "An error occured during migration");
}

app.Run();
