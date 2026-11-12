FROM python:3.12-slim
WORKDIR /srv
RUN useradd -r -u 10001 appuser
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 H4_DATABASE_URL=sqlite:////tmp/h4-demo.db
USER 10001
EXPOSE 8000
CMD ["uvicorn","energypilot.app:app","--host","0.0.0.0","--port","8000"]
