using Core.Entities;
using Core.Entities.OrderAggregate;
using System.Threading.Tasks;

namespace Core.Interfaces
{
    public interface IPaymentService
    {
        Task<CustomerBasket> CreateOrUpdatePaymentIntent(string basketId);
        Task<CustomerBasket> CreateOrUpdatePaymentIntentWithoutStripe(string basketId); // New mock method
        Task<Order> UpdateOrderPaymentSucceeded(string paymentIntentId);
        Task<Order> UpdateOrderPaymentFailed(string paymentIntentId);
    }
}
