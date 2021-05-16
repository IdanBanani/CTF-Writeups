for file in $(ls . | grep png); do
    echo "image:${file}";
    tesseract $file - | grep -i flag
done
