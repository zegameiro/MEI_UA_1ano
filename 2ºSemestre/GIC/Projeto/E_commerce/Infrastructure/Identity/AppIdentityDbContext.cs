using Core.Entities.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity;

namespace Infrastructure.Data.Identity
{
    public class AppIdentityDbContext : IdentityDbContext<AppUser>
    {
        public AppIdentityDbContext(DbContextOptions<AppIdentityDbContext> options) : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            // Ensure MySQL does not use TEXT for Identity keys
            builder.Entity<IdentityRole>(entity =>
            {
                entity.Property(r => r.Id).HasColumnType("varchar(255)");
            });

            builder.Entity<AppUser>(entity =>
            {
                entity.Property(u => u.Id).HasColumnType("varchar(255)");
            });

            builder.Entity<IdentityUserRole<string>>(entity =>
            {
                entity.Property(ur => ur.RoleId).HasColumnType("varchar(255)");
                entity.Property(ur => ur.UserId).HasColumnType("varchar(255)");
            });

            builder.Entity<IdentityUserClaim<string>>(entity =>
            {
                entity.Property(uc => uc.UserId).HasColumnType("varchar(255)");
            });

            builder.Entity<IdentityUserLogin<string>>(entity =>
            {
                entity.Property(ul => ul.UserId).HasColumnType("varchar(255)");
            });

            builder.Entity<IdentityUserToken<string>>(entity =>
            {
                entity.Property(ut => ut.UserId).HasColumnType("varchar(255)");
            });

            builder.Entity<IdentityRoleClaim<string>>(entity =>
            {
                entity.Property(rc => rc.RoleId).HasColumnType("varchar(255)");
            });
        }

    }
}