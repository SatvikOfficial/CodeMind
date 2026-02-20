FROM oven/bun:1.2.2

WORKDIR /app

COPY package.json tsconfig.json next.config.mjs postcss.config.mjs tailwind.config.ts next-env.d.ts ./
COPY app ./app
COPY components ./components
COPY hooks ./hooks
COPY lib ./lib
COPY middleware.ts ./

RUN bun install --frozen-lockfile || bun install

EXPOSE 3000

CMD ["bun", "run", "dev", "--hostname", "0.0.0.0", "--port", "3000"]
