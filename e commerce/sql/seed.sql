-- Seed data for E-Commerce Database

-- 1. Seed Categories
INSERT INTO categories (name, description, slug) VALUES 
('Electronics', 'Gadgets, smartphones, laptops, and smartwatches', 'electronics'),
('Fashion & Clothing', 'Trendy apparel for men, women, and kids', 'fashion'),
('Home & Living', 'Furniture, kitchenware, and decorative interior items', 'home-living'),
('Fitness & Sports', 'Exercise equipment, sportswear, and outdoor gear', 'fitness-sports'),
('Books & Stationery', 'Novels, journals, textbooks, and art supplies', 'books-stationery')
ON CONFLICT DO NOTHING;

-- 2. Seed Products (assuming categories IDs are 1 to 5)
-- Electronics (category_id = 1)
INSERT INTO products (name, description, price, stock, category_id, image_url, created_at, updated_at) VALUES
('Quantum Ultra Laptop', '15.6-inch screen, Intel i7 Processor, 16GB RAM, 512GB SSD, sleek metal body.', 1199.99, 15, 1, '/static/uploads/laptop.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Apex Wireless Headphones', 'Active noise cancelling, 40 hours battery life, hi-fi audio bass sound, Bluetooth 5.2.', 199.99, 25, 1, '/static/uploads/headphones.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Vanguard Smartwatch Pro', 'Heart rate monitor, GPS tracker, AMOLED screen, 14-day battery life, waterproof.', 249.99, 12, 1, '/static/uploads/smartwatch.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Fashion & Clothing (category_id = 2)
INSERT INTO products (name, description, price, stock, category_id, image_url, created_at, updated_at) VALUES
('Classic Denim Jacket', 'Heavyweight denim fabric jacket, regular fit, premium metal buttons, standard collar.', 79.99, 40, 2, '/static/uploads/denim_jacket.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Retro Running Sneakers', 'Lightweight mesh upper, flexible rubber sole, vintage aesthetics, unisex design.', 89.99, 30, 2, '/static/uploads/sneakers.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Home & Living (category_id = 3)
INSERT INTO products (name, description, price, stock, category_id, image_url, created_at, updated_at) VALUES
('Minimalist Ceramic Vase', 'Matte white handmade ceramic vase, perfect for dried flowers or modern home decor.', 34.99, 50, 3, '/static/uploads/vase.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ergonomic Office Chair', 'Breathable mesh back support, adjustable armrests, heavy-duty metal base, smooth rolling.', 189.99, 10, 3, '/static/uploads/chair.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Fitness & Sports (category_id = 4)
INSERT INTO products (name, description, price, stock, category_id, image_url, created_at, updated_at) VALUES
('Eco-Friendly Yoga Mat', 'Non-slip TPE material, double-sided texture, 6mm thickness, carrying strap included.', 29.99, 45, 4, '/static/uploads/yoga_mat.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Adjustable Dumbbell Set', 'Pair of dumbbells adjustable from 5 lbs to 52.5 lbs, textured steel handles, durable plates.', 299.99, 8, 4, '/static/uploads/dumbbell.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Books & Stationery (category_id = 5)
INSERT INTO products (name, description, price, stock, category_id, image_url, created_at, updated_at) VALUES
('Chronicles of Tomorrow', 'Sci-fi paperback bestseller novel by Arthur Pendelton. 420 pages of riveting adventure.', 14.99, 60, 5, '/static/uploads/book.webp', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
