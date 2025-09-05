# ------------------------------------
# Step 1: Build
# ------------------------------------
FROM node:18-alpine AS builder
WORKDIR /app

# ARG for build-time env
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# ------------------------------------
# Step 2: Run
# ------------------------------------
FROM node:18-alpine AS runner
WORKDIR /app

# Re-declare for runtime
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Copy only the built files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.js ./next.config.js

EXPOSE 3000
CMD ["npx", "next", "start"]