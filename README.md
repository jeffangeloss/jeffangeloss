<div align="center">

<img src="./assets/portada-viva.svg" width="100%" alt="Portada de Jefferson Sanchez. Ciencia + Tecnología + Arte = Impacto. Ingeniería de Sistemas, IA y ML, biomédica, IoT, ciberseguridad y música." />

### Jefferson Sanchez Palacios

Ingeniería de Sistemas en la Universidad de Lima, décimo superior · Lima, Perú

<img src="./assets/titular.svg" width="100%" alt="Ingeniería de Sistemas, full-stack, DevOps, IA, IoT, ciberseguridad y violista." />

<a href="https://www.linkedin.com/in/jefferson-angelo-sanchez-palacios-450728280"><img src="./assets/boton-linkedin.svg" height="40" alt="LinkedIn" /></a> <a href="mailto:jjjangelosss@gmail.com"><img src="./assets/boton-correo.svg" height="40" alt="Correo" /></a> <a href="#proyectos-destacados"><img src="./assets/boton-repos.svg" height="40" alt="Proyectos" /></a>

</div>

<table>
<tr>
<td width="50%" valign="top">

**🇵🇪 Español**

Estudiante de Ingeniería de Sistemas en la Universidad de Lima, en el décimo superior, con dos años previos de Ingeniería Biomédica. Construyo sistemas web y móviles de punta a punta, con la base de datos, las pruebas y el despliegue como parte del trabajo y no como un paso final.

Dos de mis sistemas están en producción en la universidad: el inventario de insumos químicos fiscalizados por SUNAT y la medición de resultados para la acreditación **ABET**. Fuera del código, toco la viola.

</td>
<td width="50%" valign="top">

**🇺🇸 English**

Systems Engineering student at Universidad de Lima, in the top 10% of my class, with two prior years of Biomedical Engineering. I build web and mobile systems end to end, treating the database, tests and deployment as part of the work, not as a final step.

Two of my systems run in production at the university: an inventory of SUNAT-regulated chemicals and an outcomes-measurement platform for **ABET** accreditation. Away from the keyboard, I play the viola.

</td>
</tr>
</table>

> **Abierto a · Open to:** prácticas y roles full-stack, DevOps o de datos · full-stack, DevOps and data internships or roles.

<img src="./assets/separador.svg" width="100%" alt="" />

### 🔭 Actualmente

- 👨‍💻 **Practicante de Tecnología de Procesos** en la Universidad de Lima desde julio de 2026. Desarrollo el sistema web de insumos químicos fiscalizados por SUNAT, en producción desde agosto, con React, TypeScript, una API en Hono y PostgreSQL. El código vive en repos privados.
- 📊 **Sistema de medición ABET** para la Carrera de Ingeniería Ambiental, en producción desde noviembre de 2026.
- 🤖 **MLOps** con DVC, MLflow y GitHub Actions sobre un clasificador de phishing, en el curso de DevOps.
- 🎓 Cursos de 2026-2 en DevOps, Seguridad de Sistemas, Planeamiento Estratégico y Paradigmas de Programación.

<img src="./assets/separador.svg" width="100%" alt="" />

### 🧭 Facetas

<img src="./assets/facetas.svg?v=2" width="100%" alt="Full-stack y DevOps, con ULima++ y el sistema ABET. IA, con detección de phishing en CatBoost. Biomédica, con dos años de Ingeniería Biomédica y la tesis. IoT, con un segundo factor TOTP en ESP32. Ciberseguridad, con una auditoría MASVS. Música y coctelería, como violista." />

<img src="./assets/separador.svg" width="100%" alt="" />

### 📁 Proyectos destacados

#### ⭐ Proyecto estrella · Sistema de medición ABET

<div align="center">

<a href="https://github.com/jeffangeloss/ABET-ULIMA-Back"><img src="https://img.shields.io/badge/Back-ABET--ULIMA--Back-161B22?style=for-the-badge&logo=fastapi&logoColor=8FA2FF" alt="Repositorio del Back" /></a>
<a href="https://github.com/jeffangeloss/ABET-ULIMA-Front"><img src="https://img.shields.io/badge/Front-ABET--ULIMA--Front-161B22?style=for-the-badge&logo=react&logoColor=8FA2FF" alt="Repositorio del Front" /></a>

<img src="https://img.shields.io/badge/versión-0.3.0_en_producción-2EA043?style=flat-square" alt="Versión 0.3.0 en producción" />
<img src="https://img.shields.io/badge/despliegue-Vercel-161B22?style=flat-square&logo=vercel&logoColor=8FA2FF" alt="Vercel" />
<img src="https://img.shields.io/badge/base-PostgreSQL_18_en_Neon-161B22?style=flat-square&logo=postgresql&logoColor=8FA2FF" alt="PostgreSQL 18 en Neon" />

</div>

Sistema web con el que los profesores de Ingeniería Ambiental de la Universidad de Lima cargan las evaluaciones de Blackboard y obtienen el reporte R-17 que pide la acreditación ABET. Yo defino el producto, escribo y apruebo las especificaciones y reviso cada cambio, y la implementación es asistida por IA con Claude Code.

| | Función | Qué hace |
| :---: | :--- | :--- |
| 📥 | **Carga del export** | El profesor sube el export de Blackboard de su sección y ve qué filas se aceptan y cuáles se rechazan, con el motivo. |
| 🔁 | **Carga sin duplicados** | Cada carga entra en una sola transacción, y el mismo archivo nunca se publica dos veces. |
| 📊 | **Reporte R-17** | Genera el Excel del R-17 desde la base, con una constancia que guarda la huella SHA-256 del archivo. |
| 👥 | **Roles** | El profesor ve solo sus secciones y la coordinación ve todas las cargas. |
| 🔐 | **Privacidad** | Ningún nombre de estudiante se guarda ni se muestra, y el repositorio solo usa datos inventados. |
| 🧪 | **Trazabilidad** | Nueve especificaciones; las dos últimas cruzan 32 historias de usuario y 237 escenarios con sus pruebas. |
| ⚙️ | **DevOps** | CI en GitHub Actions, migraciones con Flyway, SonarQube Cloud, respaldo programado de la base y versiones publicadas. |

```mermaid
flowchart LR
    P([Profesor]) -->|export de Blackboard| F[Front<br/>React · Vite · Tailwind]
    C([Coordinación]) --> F
    F -->|API REST| A[Back<br/>FastAPI · Python 3.12]
    A --> V{Validación<br/>fila por fila}
    V -->|aceptadas| DB[(PostgreSQL 18<br/>Neon · Flyway)]
    V -.->|rechazadas con motivo| F
    DB --> R[R-17 en Excel<br/>+ constancia SHA-256]
    R --> F
```

#### Más proyectos

<details>
<summary><b>📱 ULima++ · app académica full-stack</b></summary>
<br/>

App móvil del curso Ingeniería de Software II para consultar la vida académica en la Universidad de Lima.

| | |
| :--- | :--- |
| **Stack** | Flutter · GetX · Bun · Hono · Drizzle ORM · PostgreSQL · Vercel |
| **Lo que hice** | Autenticación con JWT y roles, la malla curricular interactiva y la API REST de 27 tablas, con 45 commits, la mayor contribución del equipo |
| **Repos** | [ULima_Frontend_IS2](https://github.com/jeffangeloss/ULima_Frontend_IS2) · [ULima_Backend_IS2](https://github.com/jeffangeloss/ULima_Backend_IS2) |

</details>

<details>
<summary><b>🤖 MLOps para la detección de phishing</b></summary>
<br/>

Proyecto final del curso de DevOps (2026-2, grupo 04), que lleva a producción el clasificador CatBoost de URL de phishing con 20 características léxicas del conjunto PhiUSIIL. Está en construcción.

| | |
| :--- | :--- |
| **Stack** | Python 3.11 · CatBoost · DVC · MLflow · GitHub Actions · FastAPI |
| **Antecedente** | El modelo del curso de Machine Learning llegó a un F1 de 0,9998 |
| **Repo** | [mlops-phishing-g4](https://github.com/jeffangeloss/mlops-phishing-g4) |

</details>

<details>
<summary><b>🧾 Punto de venta para un negocio familiar</b></summary>
<br/>

Sistema a medida para la liquidación y la cobranza diaria de Inversiones Sánchez, que atiende a más de 40 vendedores.

| | |
| :--- | :--- |
| **Stack** | Next.js · Prisma · SQLite |
| **Resultado** | Redujo en 90 % las inconsistencias en los montos cobrados |
| **Repo** | [Software-optimizacion-cobro-sanchez](https://github.com/jeffangeloss/Software-optimizacion-cobro-sanchez) |

</details>

<details>
<summary><b>🎵 Tesis · instrumento de medición en un juego rítmico</b></summary>
<br/>

Instrumento de medición de la tesis sobre un motor de juego rítmico, que registra la telemetría del ritmo y señales biométricas.

| | |
| :--- | :--- |
| **Stack** | Haxe · Python · MQTT |
| **Repo** | [Propuesta](https://github.com/jeffangeloss/Propuesta) |

</details>

<img src="./assets/separador.svg" width="100%" alt="" />

### 💬 Pregúntame sobre...

- **DevOps:** integración continua con GitHub Actions, migraciones con Flyway, análisis con SonarQube Cloud y despliegue en Vercel.
- **Bases de datos:** modelos en PostgreSQL con restricciones que validan los datos en la propia base.
- **Apps móviles:** Flutter con GetX, mapas y roles.
- **IoT:** ESP32, segundo factor TOTP y sensores.
- **Seguridad:** ISO/IEC 27001, NIST CSF 2.0, OWASP y MASVS.
- **Música:** la viola, la orquesta y cómo se cruzan con el ritmo en la tesis.

### ⚡ Datos curiosos

- 🎻 Toqué con Juan Diego Flórez en «Una Sola Fuerza» (Estadio Nacional, 2017) con Sinfonía por el Perú.
- 🧬 Llegué a Sistemas después de dos años de Ingeniería Biomédica en la PUCP y la UPCH.
- 🏆 Mis trabajos quedaron entre los 20 mejores de la feria de pósteres ExpoSistemas en 2024-2 y 2025-1.
- 📡 Lideré el área de IoT de IEEE ComSoc en la rama estudiantil de la UPC durante 2025.
- 🍸 Tengo la certificación en Bar y Coctelería de la Shaker Bartender School (2023).

<img src="./assets/separador.svg" width="100%" alt="" />

### 🧰 Tecnologías

<img src="./assets/muro-logos.svg?v=1" width="100%" alt="Muro de logos. Lenguajes: Python, TypeScript, JavaScript, Java, Dart, C, C++, Haxe y Bash. Web y móvil: React, Vite, Tailwind CSS, Next.js, Node.js, Bun, FastAPI, Spring Boot, Flutter, Firebase, HTML y CSS. Datos, IA y DevOps: PostgreSQL, SQLite, Prisma, scikit-learn, Git, GitHub, GitHub Actions, Docker, Vercel y AWS. Sistemas, IoT y herramientas: Linux, Red Hat, Kali Linux, Arduino, Raspberry Pi, VS Code, Figma y Notion." />

<div align="center">

<sub><b>Y también</b></sub><br/>
![Hono](https://img.shields.io/badge/Hono-161B22?style=flat-square&logo=hono&logoColor=8FA2FF) ![Drizzle](https://img.shields.io/badge/Drizzle-161B22?style=flat-square&logo=drizzle&logoColor=8FA2FF) ![Flyway](https://img.shields.io/badge/Flyway-161B22?style=flat-square&logo=flyway&logoColor=8FA2FF) ![SonarQube Cloud](https://img.shields.io/badge/SonarQube%20Cloud-161B22?style=flat-square&logo=sonarqubecloud&logoColor=8FA2FF) ![Snyk](https://img.shields.io/badge/Snyk-161B22?style=flat-square&logo=snyk&logoColor=8FA2FF) ![Vitest](https://img.shields.io/badge/Vitest-161B22?style=flat-square&logo=vitest&logoColor=8FA2FF) ![Playwright](https://img.shields.io/badge/Playwright-161B22?style=flat-square) ![pgTAP](https://img.shields.io/badge/pgTAP-161B22?style=flat-square) ![Neon](https://img.shields.io/badge/Neon-161B22?style=flat-square) ![CatBoost](https://img.shields.io/badge/CatBoost-161B22?style=flat-square) ![DVC](https://img.shields.io/badge/DVC-161B22?style=flat-square&logo=dvc&logoColor=8FA2FF) ![MLflow](https://img.shields.io/badge/MLflow-161B22?style=flat-square&logo=mlflow&logoColor=8FA2FF) ![pandas](https://img.shields.io/badge/pandas-161B22?style=flat-square&logo=pandas&logoColor=8FA2FF) ![Power BI](https://img.shields.io/badge/Power%20BI-161B22?style=flat-square) ![Burp Suite](https://img.shields.io/badge/Burp%20Suite-161B22?style=flat-square) ![Claude Code](https://img.shields.io/badge/Claude%20Code-161B22?style=flat-square&logo=claude&logoColor=8FA2FF)

</div>

<img src="./assets/separador.svg" width="100%" alt="" />

### 🎼 Partitura de contribuciones

<img src="https://raw.githubusercontent.com/jeffangeloss/jeffangeloss/output/partitura.svg" width="100%" alt="Partitura de contribuciones del último año. Cada nota es una semana y su altura crece con la actividad." />

<sub>Se regenera cada día con un flujo propio de GitHub Actions, sin servicios externos.</sub>

<img src="./assets/separador.svg" width="100%" alt="" />

### 📊 Estadísticas de GitHub

<img src="https://raw.githubusercontent.com/jeffangeloss/jeffangeloss/output/estadisticas.svg" width="100%" alt="Estadísticas de GitHub del último año: contribuciones, commits, pull requests, estrellas, issues, repos con commits, racha actual y racha más larga, y los lenguajes de mis repos públicos." />

<sub>Las calcula el mismo flujo diario con la API de GitHub, sin servicios externos.</sub>

<img src="./assets/separador.svg" width="100%" alt="" />

### 🌸 Animes favoritos

<img src="./assets/estante-animes.svg?v=3" width="100%" alt="Estante con los pósters de Shingeki no Kyojin, Las quintillizas, Rompiendo el hielo, Your Name, Your Lie in April, Oshi no Ko, El tiempo contigo y Evangelion, cada uno con un efecto animado: viento, destellos, nieve, cometa, pétalos, estrellas, lluvia y un campo de hexágonos." />

<img src="./assets/pie.svg" width="100%" alt="Ciencia + Tecnología + Arte = Impacto" />
