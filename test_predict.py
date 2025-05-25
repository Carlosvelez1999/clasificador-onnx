from model_utils import predict, get_label

image_path = "download.jpg"

pred_class, confidence = predict(image_path)
label = get_label(pred_class)

print(f"Clase predicha: {label} (ID: {pred_class})")
print(f"Confianza: {confidence:.2f}")
