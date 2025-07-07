using API.Dtos;
using AutoMapper;
using Core.Entities.OrderAggregate;

namespace API.Helpers
{
    public class OrderItemUrlResolver(Settings settings) : IValueResolver<OrderItem, OrderItemDto, string>
    {
        private readonly Settings _settings = settings;

        public string Resolve(OrderItem source, OrderItemDto destination, string destMember, ResolutionContext context)
        {
            if (!string.IsNullOrEmpty(source.ItemOrdered.PictureUrl))
            {
                return _settings.cdnUrl + source.ItemOrdered.PictureUrl;
            }

            return null;
        }
    }

}