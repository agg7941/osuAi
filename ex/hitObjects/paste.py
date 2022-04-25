from PIL import Image

bg = Image.open('img.png')
cursor = Image.open('cursor.png')

print(cursor.mode)
print(bg.mode)

bg.paste(cursor, (0,0), cursor)
bg.save('out.png')
