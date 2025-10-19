import streamlit as st
import json
from db import crear_tablas, registrar_usuario, validar_usuario

crear_tablas()

# Inicializar sesión
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False
    st.session_state["usuario"] = ""
    st.session_state["email"] = ""
    st.session_state["carrito"] = []

# Configuración visual
st.set_page_config(page_title="Zona90'", page_icon="👕", layout="wide")
st.title("Zona90' — Tienda de Camisetas Legendarias")
st.markdown("Bienvenido a nuestra tienda oficial de camisetas retro, modernas y de mundiales ⚽")

# Barra lateral para login/registro
opcion = st.sidebar.radio("🔐 ¿Tienes cuenta?", ["Sí", "No"])

if opcion == "Sí" and not st.session_state["logueado"]:
    st.sidebar.subheader("Inicia sesión")
    user = st.sidebar.text_input("Usuario")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Ingresar"):
        if validar_usuario(user, email, password):
            st.session_state["logueado"] = True
            st.session_state["usuario"] = user
            st.session_state["email"] = email
            st.sidebar.success(f"Bienvenido, {user}")
        else:
            st.sidebar.error("Credenciales incorrectas.")

elif opcion == "No" and not st.session_state["logueado"]:
    st.sidebar.subheader("Registro")
    nuevo_user = st.sidebar.text_input("Nuevo usuario")
    nuevo_email = st.sidebar.text_input("Correo")
    nuevo_pass = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Registrarme"):
        if registrar_usuario(nuevo_user, nuevo_email, nuevo_pass):
            st.sidebar.success("Registro exitoso. Ahora puedes iniciar sesión.")
        else:
            st.sidebar.warning("Usuario ya registrado.")

# Mostrar catálogo si está logueado
if st.session_state["logueado"]:
    st.subheader("🛍️ Catálogo de camisetas")

    with open("catalogo.json", "r") as f:
        catalogo = json.load(f)

    seccion = st.selectbox("Selecciona una sección:", list(catalogo.keys()))
    productos = catalogo[seccion]

    for nombre_producto, datos in productos.items():
        with st.container():
            st.image(datos["imagen"], width=300)
            st.markdown(f"**{nombre_producto}**")
            st.markdown(f"Precio: {datos['precio']}$")
            cantidad = st.number_input(f"Cantidad ({nombre_producto})", min_value=1, max_value=10, value=1, key=nombre_producto)

            if st.button(f"Añadir al carrito ({nombre_producto})"):
                st.session_state["carrito"].append({
                    "nombre": nombre_producto,
                    "precio": datos["precio"],
                    "cantidad": cantidad,
                    "total": datos["precio"] * cantidad
                })
                st.success(f"{nombre_producto} añadido al carrito.")

    # Mostrar carrito
    if st.session_state["carrito"]:
        st.subheader("🛒 Carrito de compras")
        total_general = 0
        for i, item in enumerate(st.session_state["carrito"]):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"{item['cantidad']} x {item['nombre']} — {item['total']}$")
            with col2:
                if st.button(f"🗑️ Eliminar {i}", key=f"del_{i}"):
                    st.session_state["carrito"].pop(i)
                    st.rerun()
            total_general += item["total"]

        st.markdown(f"**Total a pagar: {total_general}$**")
        if st.button("✅ Confirmar compra"):
            st.success(f"¡Gracias por tu compra, {st.session_state['usuario']}! Recibirás un correo a {st.session_state['email']} con los detalles.")
            st.session_state["carrito"] = []

# Pie de página
st.markdown("---")
st.markdown("© 2025 Zona90’ | Síguenos en [Instagram](https://instagram.com) • [Twitter](https://twitter.com) • [YouTube](https://youtube.com)")