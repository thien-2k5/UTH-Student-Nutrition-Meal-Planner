import sqlite3
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "food.db"

# Ensure the database directory exists
DB_PATH.parent.mkdir(exist_ok=True)

def seed_database():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Drop table if exists to restart cleanly
    cursor.execute("DROP TABLE IF EXISTS foods")

    # Create table
    cursor.execute("""
        CREATE TABLE foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            protein REAL NOT NULL,
            fat REAL NOT NULL,
            carb REAL NOT NULL,
            fiber REAL NOT NULL,
            vitamin TEXT NOT NULL,
            calories REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Food data list (at least 100 items)
    # Categories: "Sáng", "Trưa/Tối", "Ăn vặt", "Nước uống"
    foods = [
        # === BỮA SÁNG (Category: "Sáng") ===
        # Name, Price (VND), Protein (g), Fat (g), Carb (g), Fiber (g), Vitamin, Calories (kcal), Category
        ("Bánh mì ốp la (1 trứng)", 15000, 11.5, 9.8, 38.0, 1.8, "A, B12, D", 295, "Sáng"),
        ("Bánh mì ốp la (2 trứng)", 20000, 17.5, 15.0, 38.2, 1.8, "A, B12, D, E", 365, "Sáng"),
        ("Bánh mì pate chả lụa", 18000, 14.2, 12.5, 42.0, 2.0, "B1, B3, B6", 380, "Sáng"),
        ("Bánh mì xá xíu dưa chua", 22000, 16.8, 11.2, 45.0, 2.2, "B1, B3, C", 390, "Sáng"),
        ("Bánh mì chà bông bơ", 15000, 10.5, 13.0, 40.0, 1.5, "B1, B2", 320, "Sáng"),
        ("Phở bò tái nạm bình dân", 35000, 24.5, 12.0, 58.0, 2.5, "B3, B6, B12, Sắt, Kẽm", 450, "Sáng"),
        ("Phở bò viên UTH", 30000, 22.0, 10.5, 56.0, 2.2, "B3, B12, Sắt", 410, "Sáng"),
        ("Phở gà xé cải xanh", 30000, 26.0, 8.5, 55.0, 2.5, "B3, B6, A, C", 400, "Sáng"),
        ("Bún riêu cua bình dân", 30000, 15.5, 11.0, 52.0, 3.0, "A, B1, B2, Canxi", 380, "Sáng"),
        ("Bún mọc thịt băm chả chiên", 28000, 18.0, 12.5, 54.0, 2.0, "B1, B3, B6", 400, "Sáng"),
        ("Bún bò Huế sinh viên", 35000, 23.5, 13.5, 60.0, 2.5, "B3, B12, Kẽm", 480, "Sáng"),
        ("Hủ tiếu gõ xá xíu xương ống", 20000, 15.0, 9.5, 55.0, 1.8, "B1, B3", 365, "Sáng"),
        ("Hủ tiếu Nam Vang học đường", 30000, 21.0, 11.5, 57.0, 2.0, "B3, B6, Sắt", 420, "Sáng"),
        ("Xôi mặn chả lụa chà bông bơ", 15000, 12.0, 9.0, 72.0, 1.5, "B1, B3", 420, "Sáng"),
        ("Xôi xéo mỡ hành đậu xanh", 12000, 8.5, 7.5, 75.0, 3.5, "B1, B9, Sắt", 400, "Sáng"),
        ("Xôi gấc hạt sen đường cát", 12000, 6.5, 5.0, 78.0, 2.0, "Beta-carotene (A), Vitamin E", 380, "Sáng"),
        ("Cháo lòng bánh quẩy", 20000, 16.0, 14.0, 48.0, 1.2, "B12, Sắt", 380, "Sáng"),
        ("Cháo sườn băm bắc thảo", 25000, 14.5, 10.0, 45.0, 1.0, "B12, Sắt, Canxi", 330, "Sáng"),
        ("Cháo thịt bằm hành hoa", 15000, 11.0, 6.5, 42.0, 1.0, "B1, B3", 270, "Sáng"),
        ("Bánh cuốn nóng giò lụa nem chua", 25000, 13.5, 10.0, 58.0, 1.8, "B1, B3, C", 380, "Sáng"),
        ("Bánh giò thịt bằm mộc nhĩ", 15000, 9.5, 11.0, 36.0, 1.5, "B1, B3", 280, "Sáng"),
        ("Bánh bao nhân thịt trứng cút", 15000, 12.0, 9.5, 48.0, 1.2, "B1, B3, B12", 330, "Sáng"),
        ("Miến gà xé hành tây", 28000, 20.0, 7.5, 52.0, 2.0, "B3, B6", 350, "Sáng"),
        ("Nui sườn non củ cải", 30000, 18.5, 11.0, 54.0, 2.2, "B3, Sắt, C", 390, "Sáng"),
        ("Yến mạch pha sữa đặc trái cây", 18000, 9.0, 7.0, 62.0, 5.5, "B1, B5, B6, Xơ hòa tan", 350, "Sáng"),
        ("Nui xào trứng xúc xích", 20000, 13.8, 12.5, 48.0, 1.5, "A, B12, D", 360, "Sáng"),

        # === BỮA TRƯA / TỐI (Category: "Trưa/Tối") ===
        ("Cơm tấm sườn nướng mật ong", 30000, 24.5, 14.0, 68.0, 1.8, "B1, B3, B6", 510, "Trưa/Tối"),
        ("Cơm tấm sườn bì chả UTH", 35000, 29.0, 18.0, 70.0, 2.0, "B1, B3, B6, B12", 590, "Trưa/Tối"),
        ("Cơm gà xối mỡ đùi tỏi", 35000, 28.5, 22.0, 74.0, 1.5, "B3, B6, B12", 610, "Trưa/Tối"),
        ("Cơm gà xào sả ớt lá chanh", 25000, 25.0, 9.5, 65.0, 2.0, "B3, B6", 450, "Trưa/Tối"),
        ("Cơm gà luộc nước dừa + canh", 28000, 26.5, 8.0, 66.0, 2.0, "B3, B6, Kali", 440, "Trưa/Tối"),
        ("Cơm đậu hũ dồn thịt sốt cà", 22000, 18.5, 12.0, 64.0, 3.2, "Canxi, Sắt, C, E", 430, "Trưa/Tối"),
        ("Cơm ba chỉ heo kho tàu + canh", 25000, 19.5, 18.5, 62.0, 1.5, "B1, B3, B12", 500, "Trưa/Tối"),
        ("Cơm ba chỉ luộc + cà pháo + canh rau đay", 25000, 18.0, 17.5, 65.0, 3.8, "A, C, B1, B2", 490, "Trưa/Tối"),
        ("Cơm trứng đúc thịt hành lá + canh", 20000, 16.5, 11.5, 63.0, 1.5, "A, B12, D", 410, "Trưa/Tối"),
        ("Cơm cá hú kho tộ + canh chua", 28000, 22.0, 14.5, 65.0, 3.5, "A, D, Omega-3, C", 480, "Trưa/Tối"),
        ("Cơm cá nục kho cà chua + dưa leo", 22000, 21.0, 11.0, 64.0, 2.5, "B12, D, Omega-3, C", 440, "Trưa/Tối"),
        ("Cơm mực nhồi thịt sốt me", 35000, 23.5, 11.8, 66.0, 2.0, "B3, B12, Sắt", 460, "Trưa/Tối"),
        ("Cơm bò xào thiên lý tỏi thơm", 35000, 24.0, 10.5, 63.0, 3.0, "B3, B12, Sắt, C, Kẽm", 440, "Trưa/Tối"),
        ("Cơm bò lúc lắc khoai tây chiên", 40000, 25.5, 16.5, 72.0, 2.8, "B3, B12, Sắt, Kali", 540, "Trưa/Tối"),
        ("Cơm thịt bò xào bông cải xanh", 30000, 23.0, 9.8, 65.0, 4.2, "A, C, K, B12, Sắt", 440, "Trưa/Tối"),
        ("Cơm cá lóc nướng trui + mắm me", 30000, 22.5, 8.5, 66.0, 2.2, "B12, Sắt", 430, "Trưa/Tối"),
        ("Cơm chả cá thác lác rim tỏi ớt", 25000, 20.0, 9.0, 68.0, 1.8, "B12, Kali", 430, "Trưa/Tối"),
        ("Ức gà áp chảo + Khoai lang luộc + Bông cải", 30000, 32.0, 5.0, 48.0, 6.0, "A, B3, B6, C, Kali", 365, "Trưa/Tối"),
        ("Thịt kho tiêu + Canh bầu nấu tôm + Cơm", 25000, 20.5, 12.0, 68.0, 3.0, "B1, B3, C, Kẽm", 460, "Trưa/Tối"),
        ("Cá lóc kho tộ + Canh bí đỏ thịt bằm + Cơm", 28000, 23.0, 11.5, 70.0, 3.8, "A, B12, C, Kali", 475, "Trưa/Tối"),
        ("Cơm chiên Dương Châu lạp xưởng", 25000, 14.5, 16.0, 78.0, 2.0, "B1, B2, A", 515, "Trưa/Tối"),
        ("Cơm chiên hải sản trứng muối", 30000, 19.5, 14.5, 76.0, 1.8, "A, B12, Sắt", 510, "Trưa/Tối"),
        ("Cơm bò kho bánh mì", 35000, 25.0, 15.0, 58.0, 2.5, "B3, B12, A, Sắt", 470, "Trưa/Tối"),
        ("Bún thịt nướng chả giò hành mỡ", 28000, 19.0, 14.0, 62.0, 3.0, "B1, B3, C", 450, "Trưa/Tối"),
        ("Bún chả giò chay (đậu hũ nấm)", 20000, 9.5, 9.0, 65.0, 4.5, "Canxi, Sắt, Xơ", 380, "Trưa/Tối"),
        ("Mì xào thịt bò rau cải ngọt", 25000, 20.0, 11.0, 64.0, 3.2, "B12, Sắt, A, C", 435, "Trưa/Tối"),
        ("Mì xào giòn hải sản giá hẹ", 35000, 21.5, 13.0, 68.0, 2.8, "B12, Kẽm, C", 475, "Trưa/Tối"),
        ("Nui xào bò hành tây xốt cà", 25000, 20.5, 10.5, 60.0, 2.2, "B3, B12, Sắt, C", 415, "Trưa/Tối"),
        ("Bún đậu mắm tôm thập cẩm sinh viên", 35000, 22.0, 18.5, 65.0, 3.0, "Canxi, Sắt, B1", 515, "Trưa/Tối"),
        ("Cơm cá điêu hồng chiên xù + mắm xoài", 25000, 21.5, 10.0, 66.0, 2.5, "B12, Omega-3, C", 440, "Trưa/Tối"),
        ("Cơm trứng ốp la xào hành tây sốt dầu hào", 15000, 11.8, 9.5, 62.0, 1.8, "A, B12, D", 380, "Trưa/Tối"),
        ("Cơm đùi gà chiên nước mắm + dưa leo", 30000, 27.0, 18.5, 68.0, 1.8, "B3, B6, B12", 545, "Trưa/Tối"),
        ("Cơm sườn rim mặn ngọt + Đậu cô ve xào", 25000, 21.0, 11.5, 68.0, 3.2, "B1, B3, A, K", 460, "Trưa/Tối"),
        ("Cơm nạc heo rim sả ớt + Canh rau ngót", 25000, 22.5, 9.0, 67.0, 3.5, "B1, B3, A, C, Sắt", 440, "Trưa/Tối"),
        ("Cơm thịt viên sốt cà chua + Canh cải cúc", 22000, 18.0, 12.5, 65.0, 3.0, "B1, B3, C, Sắt", 445, "Trưa/Tối"),
        ("Cơm lòng gà xào mướp giá + canh", 20000, 15.5, 9.8, 64.0, 3.5, "A, B12, Sắt, C", 405, "Trưa/Tối"),
        ("Cơm chả trứng hấp nấm mèo thịt băm", 20000, 16.5, 11.0, 65.0, 2.2, "A, B12, D", 425, "Trưa/Tối"),
        ("Cơm tép rang lá chanh + Canh bí xanh", 22000, 17.0, 6.5, 66.0, 3.0, "Canxi, Sắt, C", 390, "Trưa/Tối"),
        ("Cơm cá bạc má chiên + Canh mướp đắng", 25000, 23.0, 9.5, 65.0, 3.5, "Omega-3, B12, C", 435, "Trưa/Tối"),
        ("Cơm thịt xá xíu rim mật ong + rau luộc", 28000, 22.0, 12.0, 68.0, 2.8, "B1, B3, A, C", 470, "Trưa/Tối"),
        ("Cơm cá ngừ kho thơm (khóm) + rau thơm", 25000, 24.5, 8.5, 66.0, 3.0, "Omega-3, B12, C, Kali", 440, "Trưa/Tối"),
        ("Cơm sườn sụn rim tiêu + Canh cải ngọt", 30000, 22.0, 13.5, 67.0, 3.2, "B1, B3, C, Sắt", 475, "Trưa/Tối"),
        ("Cơm thịt bò xào đậu rồng tỏi", 28000, 21.5, 10.0, 65.0, 3.6, "B12, Sắt, A, C, Canxi", 435, "Trưa/Tối"),
        ("Cơm đậu hũ sốt nấm đông cô chay", 18000, 10.5, 7.5, 68.0, 4.0, "D, Kali, Canxi", 380, "Trưa/Tối"),
        ("Cơm rau củ luộc kho quẹt tóp mỡ", 20000, 8.5, 14.0, 72.0, 5.0, "A, C, K, Canxi", 450, "Trưa/Tối"),
        ("Bún cá miền Tây phi lê chiên giòn", 30000, 21.0, 9.0, 62.0, 2.5, "B12, Sắt, A", 415, "Trưa/Tối"),
        ("Bún măng vịt sả ớt sinh viên", 35000, 23.5, 17.0, 60.0, 3.2, "B3, B6, Kali", 490, "Trưa/Tối"),
        ("Bún kèn Phú Quốc ngon thơm nước cốt dừa", 35000, 18.5, 15.0, 65.0, 2.8, "Kali, Sắt, B12", 470, "Trưa/Tối"),
        ("Mì Quảng gà trứng cút đậu phộng", 30000, 22.5, 13.0, 58.0, 2.5, "B3, B12, Sắt, E", 440, "Trưa/Tối"),
        ("Hủ tiếu chay đậu hũ nấm rơm rau củ", 20000, 9.5, 6.0, 64.0, 4.0, "Canxi, Kali, C", 350, "Trưa/Tối"),

        # === ĂN VẶT / PHỤ (Category: "Ăn vặt") ===
        ("Trứng gà luộc (1 quả)", 5000, 6.3, 5.3, 0.6, 0.0, "A, B12, D, E", 75, "Ăn vặt"),
        ("Trứng vịt lộn luộc + rau răm + muối tiêu", 10000, 13.6, 12.4, 2.1, 0.5, "A, B12, Sắt, Beta-carotene", 182, "Ăn vặt"),
        ("Chuối già hương chín (1 quả vừa)", 3000, 1.2, 0.3, 27.0, 3.0, "B6, C, Kali", 105, "Ăn vặt"),
        ("Khoai lang mật vàng luộc (1 củ vừa)", 6000, 2.0, 0.2, 26.0, 3.8, "A, C, Kali, Mangan", 112, "Ăn vặt"),
        ("Đậu hũ non luộc sả gừng", 5000, 8.0, 4.8, 1.9, 1.2, "Canxi, Sắt, Magie", 85, "Ăn vặt"),
        ("Đậu hũ chiên giòn xóc sả ớt", 7000, 9.5, 9.0, 2.5, 1.2, "Canxi, Sắt", 130, "Ăn vặt"),
        ("Bắp nếp luộc mỡ hành", 8000, 3.5, 3.0, 38.0, 3.5, "B1, B5, Folate", 190, "Ăn vặt"),
        ("Bánh tráng trộn khô bò trứng cút", 15000, 6.5, 8.5, 48.0, 1.5, "A, B12, C", 295, "Ăn vặt"),
        ("Gỏi cuốn tôm thịt hẹ (2 cuốn)", 12000, 9.0, 3.5, 24.0, 1.8, "B12, C, Sắt", 160, "Ăn vặt"),
        ("Bánh tráng nướng mắm ruốc trứng cút", 15000, 7.5, 9.5, 36.0, 1.2, "A, B12, Sắt", 260, "Ăn vặt"),
        ("Há cảo hấp nhân tôm thịt (6 cái)", 18000, 11.5, 6.5, 32.0, 1.0, "B12, Sắt", 235, "Ăn vặt"),
        ("Bánh giò nóng thịt mộc nhĩ dưa leo", 15000, 9.0, 11.2, 35.0, 1.5, "B1, B3", 275, "Ăn vặt"),
        ("Sữa chua có đường Vinamilk (1 hũ)", 8000, 3.5, 3.0, 15.0, 0.0, "Canxi, D, B2, B12", 100, "Ăn vặt"),
        ("Sữa chua nếp cẩm hạt sen", 15000, 4.5, 3.5, 34.0, 2.0, "Canxi, B1, Sắt", 185, "Ăn vặt"),
        ("Rong biển sấy tỏi ăn liền (1 gói)", 12000, 3.0, 2.0, 6.0, 2.5, "A, C, Canxi, I-ốt", 54, "Ăn vặt"),
        ("Hạt điều rang muối vỏ lụa (50g)", 20000, 9.0, 22.0, 15.0, 1.6, "E, K, Magie, Kẽm", 290, "Ăn vặt"),
        ("Đậu phộng rang tỏi ớt lá chanh (50g)", 10000, 12.0, 24.0, 8.0, 4.2, "E, B3, Folate", 300, "Ăn vặt"),
        ("Trái cây tô sữa chua (Dưa hấu, xoài, mít)", 25000, 4.0, 3.2, 38.0, 4.0, "A, C, Kali", 195, "Ăn vặt"),
        ("Chè mè đen nước cốt dừa (chè sủi)", 10000, 3.5, 6.5, 36.0, 2.8, "Canxi, Magie, E", 215, "Ăn vặt"),
        ("Chè đậu xanh đánh nước cốt dừa", 10000, 5.0, 4.5, 42.0, 3.5, "B1, B9, Sắt, Kali", 225, "Ăn vặt"),
        ("Đậu nành edamame luộc muối (100g)", 15000, 11.0, 5.0, 10.0, 5.0, "K, Folate, Sắt, Canxi", 130, "Ăn vặt"),

        # === NƯỚC UỐNG (Category: "Nước uống") ===
        ("Sữa đậu nành UTH tự nấu", 6000, 6.5, 4.0, 12.0, 1.5, "B1, B2, E, Phytoestrogen", 110, "Nước uống"),
        ("Sữa bắp non ngọt mát ngon", 8000, 2.2, 3.0, 24.0, 1.2, "A, B1", 130, "Nước uống"),
        ("Sữa tươi tiệt trùng TH True Milk (180ml)", 9000, 6.0, 6.0, 9.0, 0.0, "Canxi, D3, B12", 114, "Nước uống"),
        ("Sinh tố bơ nước cốt dừa sữa đặc", 20000, 3.5, 18.0, 32.0, 4.5, "E, Kali, Monounsaturated Fat", 300, "Nước uống"),
        ("Sinh tố chuối sữa chua hạt chia", 18000, 4.5, 4.0, 38.0, 5.2, "B6, C, Kali, Omega-3", 200, "Nước uống"),
        ("Sinh tố xoài cát sữa tươi", 18000, 2.5, 2.8, 36.0, 2.5, "A, C, E, Folate", 180, "Nước uống"),
        ("Sinh tố đu đủ chanh dây", 15000, 1.8, 1.0, 28.0, 3.0, "A, C, Papain enzyme", 125, "Nước uống"),
        ("Nước mía siêu sạch vị tắc (quất)", 7000, 0.5, 0.2, 32.0, 0.8, "C, Sắt, Kali", 130, "Nước uống"),
        ("Nước dừa xiêm ngọt nguyên trái", 15000, 0.7, 0.2, 12.0, 2.0, "Kali, Magie, Natri", 50, "Nước uống"),
        ("Nước cam sành vắt đường đá", 15000, 1.0, 0.2, 28.0, 1.0, "C, Kali, Folate", 115, "Nước uống"),
        ("Nước chanh dây chua ngọt hạt chia", 12000, 1.2, 1.5, 22.0, 2.5, "A, C, Xơ hòa tan", 105, "Nước uống"),
        ("Trà tắc mật ong thanh mát đá", 10000, 0.2, 0.1, 18.0, 0.5, "C, Kháng khuẩn", 75, "Nước uống"),
        ("Trà đào sả hạt chia đá ngọt", 15000, 0.4, 0.5, 24.0, 1.2, "C, Kali", 100, "Nước uống"),
        ("Cà phê sữa đá Sài Gòn UTH", 12000, 2.0, 3.5, 22.0, 0.0, "Caffeine, B3", 125, "Nước uống"),
        ("Cà phê đen đá ít đường tỉnh táo", 10000, 0.5, 0.1, 8.0, 0.0, "Caffeine, Chất chống oxy hóa", 35, "Nước uống"),
        ("Trà đá mát lạnh UTH", 2000, 0.0, 0.0, 0.0, 0.0, "Chất chống oxy hóa", 0, "Nước uống"),
        ("Trà sữa truyền thống trân châu đen", 20000, 2.5, 8.0, 48.0, 0.5, "Canxi", 270, "Nước uống"),
        ("Sữa chua uống Proby men sống", 7000, 1.2, 0.8, 14.0, 0.0, "Probiotics, Vitamin D3", 68, "Nước uống")
    ]

    cursor.executemany("""
        INSERT INTO foods (name, price, protein, fat, carb, fiber, vitamin, calories, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, foods)

    conn.commit()
    
    # Verify count
    cursor.execute("SELECT COUNT(*) FROM foods")
    count = cursor.fetchone()[0]
    print(f"Successfully seeded {count} food items into foods table.")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    seed_database()
