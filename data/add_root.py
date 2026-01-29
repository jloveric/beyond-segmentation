for dataset, n in zip(["b", "x"], [378, 228]):
    for image_num in range(1, n + 1):
        with open(f"{dataset}/cmp_{dataset}{image_num:0{4}d}.xml", "r+") as file:
            content = file.read()
            file.seek(0)
            file.write("<root>\n" + content + "</root>\n")
