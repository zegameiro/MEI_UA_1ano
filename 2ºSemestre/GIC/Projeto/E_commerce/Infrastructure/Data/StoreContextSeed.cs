using System.Text.Json;
using Core.Entities;
using Core.Entities.OrderAggregate;
using Infrastructure.Data;

namespace Infrastructure.Data
{
    public class StoreContextSeed
    {
        public static async Task SeedAsync(StoreContext context)
        {   
            var kSettings = new KSettings();
            if (!context.ProductBrands.Any())
            {
                Console.WriteLine("Seeding product brands...");
                var brandsData = File.ReadAllText(kSettings.seedDataPath + "/brands.json");
                var brands = JsonSerializer.Deserialize<List<ProductBrand>>(brandsData);
                context.ProductBrands.AddRange(brands);
            }

            if (!context.ProductTypes.Any())
            {
                Console.WriteLine("Seeding product types...");
                var typesData = File.ReadAllText(kSettings.seedDataPath + "/types.json");
                var types = JsonSerializer.Deserialize<List<ProductType>>(typesData);
                context.ProductTypes.AddRange(types);
            }

            if (!context.Products.Any())
            {
                Console.WriteLine("Seeding products...");
                var productsData = File.ReadAllText(kSettings.seedDataPath + "/products.json");
                var products = JsonSerializer.Deserialize<List<Product>>(productsData);
                context.Products.AddRange(products);
            }

            if (!context.DeliveryMethods.Any())
            {   
                Console.WriteLine("Seeding delivery methods...");
                var deliveryData = File.ReadAllText(kSettings.seedDataPath + "/delivery.json");
                var methods = JsonSerializer.Deserialize<List<DeliveryMethod>>(deliveryData);
                context.DeliveryMethods.AddRange(methods);
            }

            if (context.ChangeTracker.HasChanges()) await context.SaveChangesAsync();
        }
    }
}