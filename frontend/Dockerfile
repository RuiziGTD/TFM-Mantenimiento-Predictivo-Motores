# ETAPA 1: Construcción (Build)
FROM node:22-alpine as build
WORKDIR /app

# Copiamos dependencias primero para aprovechar caché de Docker
COPY package.json package-lock.json ./
RUN npm install

# Copiamos el resto del código y construimos
COPY . .
RUN npm run build -- --configuration production

# ETAPA 2: Servidor Web (Nginx)
FROM nginx:alpine

# Copiamos los archivos compilados de Angular al servidor Nginx
# El '*' es un comodín para que no importe cómo se llame tu proyecto en angular.json
# NOTA: Angular 17+ genera la carpeta 'browser'. Si te da error, borra '/browser' de la ruta.
COPY --from=build /app/dist/*/browser /usr/share/nginx/html

# Copiamos nuestra configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]