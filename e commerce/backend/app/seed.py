import os
from PIL import Image, ImageDraw
from backend.app.database import db
from backend.app.models.category import Category
from backend.app.models.product import Product

def create_gradient_image(filepath, text, bg_start=(41, 128, 185), bg_end=(155, 89, 182)):
    """
    Creates a 400x300 image with a smooth linear gradient and text in the center.
    This serves as a beautiful placeholder image for products.
    """
    width, height = 400, 300
    base = Image.new('RGB', (width, height), bg_start)
    top = Image.new('RGB', (width, height), bg_end)
    
    # Draw linear gradient
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        # Linear transition from top (0) to bottom (255)
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    
    # Composite the two colored images using the mask
    image = Image.composite(base, top, mask)
    draw = ImageDraw.Draw(image)
    
    # Draw standard simple icon/shapes based on product category/name
    # Draw a matching abstract icon shape in the center
    icon_color = (255, 255, 255, 180)
    if 'Laptop' in text:
        # Laptop shape
        draw.rectangle([140, 110, 260, 170], outline=icon_color, width=4)
        draw.line([120, 172, 280, 172], fill=icon_color, width=6)
    elif 'Headphones' in text:
        # Headphone shape
        draw.arc([140, 100, 260, 220], start=180, end=0, fill=icon_color, width=5)
        draw.ellipse([130, 160, 155, 200], fill=icon_color)
        draw.ellipse([245, 160, 270, 200], fill=icon_color)
    elif 'Watch' in text:
        # Watch shape
        draw.rectangle([185, 90, 215, 210], fill=icon_color)
        draw.ellipse([170, 120, 230, 180], fill=icon_color, outline=(255,255,255), width=2)
    elif 'Chair' in text:
        # Chair shape
        draw.line([170, 120, 230, 120], fill=icon_color, width=4)
        draw.line([170, 120, 170, 180], fill=icon_color, width=4)
        draw.line([230, 120, 230, 180], fill=icon_color, width=4)
        draw.line([185, 150, 215, 150], fill=icon_color, width=4)
    else:
        # Generic box/diamond
        draw.polygon([200, 100, 250, 150, 200, 200, 150, 150], outline=icon_color, width=3)
        
    # Save image
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    image.save(filepath, 'WEBP')

def seed_database():
    """Seeds categories, products, and generates real static images if they don't exist."""
    print("Database seeding started...")
    
    # 1. Seed Categories
    default_categories = [
        {'name': 'Electronics', 'description': 'Gadgets, smartphones, laptops, and smartwatches', 'slug': 'electronics'},
        {'name': 'Fashion & Clothing', 'description': 'Trendy apparel for men, women, and kids', 'slug': 'fashion'},
        {'name': 'Home & Living', 'description': 'Furniture, kitchenware, and decorative interior items', 'slug': 'home-living'},
        {'name': 'Fitness & Sports', 'description': 'Exercise equipment, sportswear, and outdoor gear', 'slug': 'fitness-sports'},
        {'name': 'Books & Stationery', 'description': 'Novels, journals, textbooks, and art supplies', 'slug': 'books-stationery'}
    ]
    
    category_map = {}
    for cat_data in default_categories:
        cat = Category.query.filter_by(slug=cat_data['slug']).first()
        if not cat:
            cat = Category(name=cat_data['name'], description=cat_data['description'], slug=cat_data['slug'])
            db.session.add(cat)
            db.session.flush()  # populate ID
        category_map[cat_data['slug']] = cat
    
    db.session.commit()
    
    # 2. Seed Products
    default_products = [
        {
            'name': 'Quantum Ultra Laptop',
            'description': '15.6-inch screen, Intel i7 Processor, 16GB RAM, 512GB SSD, sleek metal body. Perfect for work and gaming.',
            'price': 1199.99,
            'stock': 15,
            'category_slug': 'electronics',
            'filename': 'laptop.webp',
            'gradient': ((44, 62, 80), (52, 152, 219)) # Dark blue gradient
        },
        {
            'name': 'Apex Wireless Headphones',
            'description': 'Active noise cancelling, 40 hours battery life, hi-fi audio bass sound, Bluetooth 5.2. Comfortable ear cushion layout.',
            'price': 199.99,
            'stock': 25,
            'category_slug': 'electronics',
            'filename': 'headphones.webp',
            'gradient': ((41, 128, 185), (155, 89, 182)) # Purple/blue gradient
        },
        {
            'name': 'Vanguard Smartwatch Pro',
            'description': 'Heart rate monitor, GPS tracker, AMOLED screen, 14-day battery life, waterproof. Built-in sports activity metrics.',
            'price': 249.99,
            'stock': 12,
            'category_slug': 'electronics',
            'filename': 'smartwatch.webp',
            'gradient': ((26, 188, 156), (46, 204, 113)) # Emerald/Green gradient
        },
        {
            'name': 'Classic Denim Jacket',
            'description': 'Heavyweight denim fabric jacket, regular fit, premium metal buttons, standard collar. Rugged and versatile.',
            'price': 79.99,
            'stock': 40,
            'category_slug': 'fashion',
            'filename': 'denim_jacket.webp',
            'gradient': ((192, 57, 43), (230, 126, 34)) # Orange/red gradient
        },
        {
            'name': 'Retro Running Sneakers',
            'description': 'Lightweight mesh upper, flexible rubber sole, vintage aesthetics, unisex design. Premium cushioning for runners.',
            'price': 89.99,
            'stock': 30,
            'category_slug': 'fashion',
            'filename': 'sneakers.webp',
            'gradient': ((243, 156, 18), (241, 196, 15)) # Yellow gradient
        },
        {
            'name': 'Minimalist Ceramic Vase',
            'description': 'Matte white handmade ceramic vase, perfect for dried flowers or modern home decor. Adds a sophisticated touch.',
            'price': 34.99,
            'stock': 50,
            'category_slug': 'home-living',
            'filename': 'vase.webp',
            'gradient': ((142, 68, 173), (44, 62, 80)) # Dark violet gradient
        },
        {
            'name': 'Ergonomic Office Chair',
            'description': 'Breathable mesh back support, adjustable armrests, heavy-duty metal base, smooth rolling casters. Relieves back strain.',
            'price': 189.99,
            'stock': 10,
            'category_slug': 'home-living',
            'filename': 'chair.webp',
            'gradient': ((52, 73, 94), (127, 140, 141)) # Slate grey gradient
        },
        {
            'name': 'Eco-Friendly Yoga Mat',
            'description': 'Non-slip TPE material, double-sided texture, 6mm thickness, carrying strap included. Biodegradable and odorless.',
            'price': 29.99,
            'stock': 45,
            'category_slug': 'fitness-sports',
            'filename': 'yoga_mat.webp',
            'gradient': ((39, 174, 96), (26, 188, 156)) # Teal gradient
        },
        {
            'name': 'Adjustable Dumbbell Set',
            'description': 'Pair of dumbbells adjustable from 5 lbs to 52.5 lbs, textured steel handles, durable plates. Saves storage space.',
            'price': 299.99,
            'stock': 8,
            'category_slug': 'fitness-sports',
            'filename': 'dumbbell.webp',
            'gradient': ((44, 62, 80), (127, 140, 141)) # Dark grey gradient
        },
        {
            'name': 'Chronicles of Tomorrow',
            'description': 'Sci-fi paperback bestseller novel by Arthur Pendelton. 420 pages of riveting space exploration and futuristic details.',
            'price': 14.99,
            'stock': 60,
            'category_slug': 'books-stationery',
            'filename': 'book.webp',
            'gradient': ((22, 160, 133), (44, 62, 80)) # Forest/teal gradient
        }
    ]
    
    # Target directory for generated images
    base_dir = os.path.abspath(os.path.dirname(__file__))
    uploads_dir = os.path.join(base_dir, 'static', 'uploads')
    
    for prod_data in default_products:
        prod = Product.query.filter_by(name=prod_data['name']).first()
        image_relative_path = f"/static/uploads/{prod_data['filename']}"
        image_absolute_path = os.path.join(uploads_dir, prod_data['filename'])
        
        # 1. Generate image if file does not exist
        if not os.path.exists(image_absolute_path):
            try:
                print(f"Generating image asset: {prod_data['filename']}")
                create_gradient_image(
                    image_absolute_path, 
                    prod_data['name'], 
                    bg_start=prod_data['gradient'][0], 
                    bg_end=prod_data['gradient'][1]
                )
            except Exception as e:
                print(f"Failed to generate image: {str(e)}")
                image_relative_path = '/static/uploads/placeholder.webp'
        
        # 2. Save product to database
        if not prod:
            cat = category_map[prod_data['category_slug']]
            prod = Product(
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                stock=prod_data['stock'],
                category_id=cat.id,
                image_url=image_relative_path
            )
            db.session.add(prod)
            
    db.session.commit()
    print("Database seeding completed.")
