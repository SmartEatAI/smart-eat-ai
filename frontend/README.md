# SmartEat AI Frontend

Este frontend implementa la interfaz de usuario de SmartEat AI, una plataforma de recomendaciones nutricionales personalizadas basada en inteligencia artificial.

## Descripción

La aplicación está desarrollada con Next.js y TypeScript, utilizando Tailwind CSS para el diseño y una arquitectura modular basada en componentes. Permite a los usuarios gestionar su perfil, consultar planes nutricionales, interactuar con un chat inteligente y visualizar recetas y estadísticas personalizadas.

## Estructura principal

```
frontend/
├── app/                # Páginas y layouts principales (Next.js App Router)
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── (authroute)/    # Rutas públicas (login, registro)
│   └── (protected)/    # Rutas protegidas (dashboard, chat, perfil, plan)
├── components/         # Componentes reutilizables
│   ├── auth/           # Formularios y protección de rutas
│   ├── chat/           # Chat y mensajes
│   ├── layout/         # Navbar, sidebar, footer
│   ├── my-plan/        # Visualización de planes
│   ├── profile/        # Secciones de perfil
│   └── ui/             # Elementos de UI y tarjetas
├── context/            # Contextos globales (auth, perfil)
├── hooks/              # Custom hooks (useAuth, useProfile)
├── lib/                # Utilidades
├── public/             # Recursos estáticos (imágenes)
├── schemas/            # Esquemas de validación
├── types/              # Tipos TypeScript compartidos
├── package.json        # Dependencias y scripts
├── tailwind.config.js  # Configuración de Tailwind CSS
├── next.config.ts      # Configuración de Next.js
└── tsconfig.json       # Configuración de TypeScript
```

## Características principales

- Autenticación y protección de rutas
- Gestión y edición de perfil de usuario
- Visualización y seguimiento de planes nutricionales
- Chat inteligente para recomendaciones y consultas
- Visualización de recetas y estadísticas
- Interfaz moderna, responsive y accesible

## Instalación y desarrollo local

1. Instala las dependencias:
   ```bash
   npm install
   ```
2. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```
3. Accede a la app en [https://smart-eat-ai.vercel.app](https://smart-eat-ai.vercel.app)

> **Nota:** Si usas Docker, consulta el README principal del proyecto para instrucciones de despliegue con contenedores.

## Stack tecnológico

- **Next.js** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **React Context API**
- **ESLint, Prettier**

## Estructura de rutas

- `/` — Landing page
- `/auth` — Login y registro
- `/dashboard` — Panel principal del usuario
- `/my-plan` — Plan nutricional personalizado
- `/profile` — Perfil y preferencias
- `/chat` — Chat inteligente
