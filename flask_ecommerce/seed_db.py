from app import create_app, db
from app.models import Product
app = create_app()

products = [
    Product(name="HP EliteBook x360 1030 G3", price=500000, description="13.3 bendable touchscreen laptop,intel core i7, 16GB RAM, 512GB ROM", image="static/img/laptop.jpg", stock=50),
    Product(name="Apple iPad 10th Gen (Wi-Fi, 64GB)", price=15000000, description="10.9-inch Liquid Retina display, A14 Bionic chip for smooth performance, and all-day battery life — perfect for work, play, and creativity", image="static/img/phone.jpg", stock=60),
    Product(name="EchoSound Pro Wireless Headphones", price=50000, description="Active noise-cancellation,up to 20hours of battery life and a comfortable over-ear design for all day listening", image="static/img/headphones.jpg", stock=35),
    Product(name="PulseX Smartwatch Series 5", price=80000, description="Stay Connected and track your health with the PulseX Smartwatch Serires 5", image="static/img/smartwatch.jpg", stock=35),
    Product(name="PlayStation 4 Slim Console (500GB)", price=600000, description="Level up your gaming with the PlayStation 4 Slim. With 500GB of storage, stunning HDR visuals, and access to top-tier title", image="static/img/ps4console.jpg", stock=45),
    Product(name="RGB Gaming Keyboard", price=15000, description="RGB backlit gaming keyboard", image="static/img/keyboard.jpg", stock=25),
    Product(name="Zealot S39 Pro Bluetooth Speaker", price=80000, description="High-quality sound output,Fill any space with rich, clear sound using the BassBlaze Portable Bluetooth Speaker. With deep bass, 12-hour battery life, and water-resistant design, it’s perfect for parties, outdoor adventures, and everyday listening", image="static/img/speaker.jpg", stock=18),
    Product(name="VoltEdge 20K Power Bank", price=30000, description="High-capacity 20,000mAh power bank with dual USB output, fast charging, and LED battery indicator", image="static/img/powerbank.jpg", stock=35),
    Product(name="DataCore 1TB External Hard Drive", price=120000, description="Secure and reliable 1TB external hard drive with USB 3.0 high-speed transfer and backups", image="static/img/harddrive.jpg", stock=25),
    Product(name="AirPods Pro (2nd Gen) – Wireless Earbuds", price=100000, description="Enjoy immersive sound with AirPods Pro. Features Active Noise Cancellation", image="static/img/airpods.jpg", stock=50),
    Product(name="VisionX 50” 4K UHD Smart TV", price=350000, description="Bring your entertainment to life with the VisionX 50-inch Smart TV. Featuring ultra-clear 4K resolution, built-in Wi-Fi and vibrant HDR color", image="static/img/smarttv.jpg", stock=50),
    Product(name="TitanBox X Gaming Console", price=300000, description="Dominate the game with the TitanBox X. Featuring ultra-fast load times, 4K gaming support, and a powerful multi-core processor", image="static/img/console.jpg", stock=40),
    Product(name="GlidePro Silent Wireless Mouse", price=55000, description="Work and play with precision using the GlidePro Wireless Mouse. Features silent clicks, adjustable DPI settings, ergonomic grip, and long battery life", image="static/img/mouse.jpg", stock=48),
    Product(name="Xbox Vortex Series X", price=95000, description="Unleash next-gen power with the Xbox Vortex Series X. Engineered for 4K gaming, lightning-fast load times", image="static/img/xboxconsole.jpg", stock=12),
    Product(name="Adidas StrideFlex Runner", price=50000, description="Built for speed and comfort, the Adidas StrideFlex Runner features breathable mesh", image="static/img/shoe.jpg", stock=12),
    Product(name="Xbox PulseStrike Wireless Controller", price=50000, description="Precision meets comfort with the Xbox PulseStrike Wireless Controller", image="static/img/xbox.jpg", stock=14),
    Product(name="Sony PS5 Controller- DualSense Wireless Pad- PlayStation 5- White", price=500000, description="Experience the next level of gaming with the PlayStation 5 DualSense Wireless Controller. Featuring advanced haptic feedback, adaptive triggers, and a sleek ergonomic design, the DualSense delivers immersive gameplay like never before. Includes a built-in microphone, USB-C charging, and a responsive touchpad. Designed for precision, comfort, and complete control.", image="static/img/controller.jpg", stock=40),
    Product(name="GripMaster Pro Thumbsleeves", price=8000, description="Enhance your mobile gaming precision and comfort with GripMaster Pro Thumbsleeves(6 Pairs)", image="static/img/thumbsleeves.jpg", stock=60),
    Product(name="Eageat TurboCharge USB-C Fast Charger", price=12000, description="Power up quickly with the Eageat TurboCharge USB-C Fast Charger. Compact, efficient, and compatible with most smartphones and tablets — it delivers fast, safe charging wherever you go", image="static/img/flash.jpg", stock=47),
    Product(name="LuminaBeam Portable Projector", price=89000, description="Take your movies, games, and presentations anywhere with the LuminaBeam Portable Projector. Compact yet powerful, it delivers sharp 1080p visuals, built-in speakers, and easy connectivity — perfect for on-the-go entertainment", image="static/img/projector.jpg", stock=30),
    

]
# Insert into database
with app.app_context():
    db.session.add_all(products)
    db.session.commit()
    print("Database seeded successfully")