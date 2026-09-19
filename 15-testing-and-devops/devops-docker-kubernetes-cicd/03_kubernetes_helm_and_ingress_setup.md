# Kubernetes Production Deployment: Helm Charts, Ingress, and HPA

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Kubernetes ek **Container Cargo Ship ka Captain** hai:
- **Pod**: Ek container box jisme aapka application code chal raha hai.
- **Service**: Ek internal intercom phone number taaki doosre containers isse baat kar sakein.
- **Ingress Controller (NGINX)**: Port ka security gate jo internet se aane wale URL (`https://api.domain.com`) ko sahi container tak pahunchata hai.
- **HPA (Horizontal Pod Autoscaler)**: Captain dekhta hai ki load badh raha hai, toh wo 2 pods ki jagah 10 pods auto-scale kar deta hai!

---

## 💻 2. Line-by-Line Commented Kubernetes Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knowledgebase-api
  labels:
    app: knowledgebase-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: knowledgebase-api
  template:
    metadata:
      labels:
        app: knowledgebase-api
    spec:
      containers:
        - name: web
          image: ghcr.io/iamjayprakash/knowledgebase:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
---
# hpa.yaml - Horizontal Pod Autoscaler based on CPU
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: knowledgebase-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: knowledgebase-api
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 75
```
