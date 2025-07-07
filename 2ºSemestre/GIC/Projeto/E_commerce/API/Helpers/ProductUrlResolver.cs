using API.Dtos;
using AutoMapper;
using Core.Entities;
using Microsoft.Extensions.Configuration;

namespace API.Helpers
{
    public class ProductUrlResolver(Settings settings) : IValueResolver<Product, ProductToReturnDto, string>
    {
        private readonly Settings _settings = settings;

        public string Resolve(Product source, ProductToReturnDto destination, string destMember, ResolutionContext context)
        {
            if (!string.IsNullOrEmpty(source.PictureUrl))
            {
                return _settings.cdnUrl + source.PictureUrl;
            }
            return null;
        }
    }
}