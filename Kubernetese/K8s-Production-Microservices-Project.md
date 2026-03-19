# 🚀 Production-Ready Microservices on Kubernetes
### End-to-End Portfolio Project | SRE/DevOps Interview Level

---

## Architecture Overview

```
                         Internet
                             │
                    ┌────────▼────────┐
                    │  NGINX Ingress  │  (TLS termination, rate limiting)
                    │  taskapp.local  │
                    └────┬───────┬───┘
                         │       │
              /api/*      │       │  /*
                    ┌─────▼──┐  ┌▼────────┐
                    │Backend │  │Frontend │
                    │(2-10   │  │(2 pods) │
                    │ pods)  │  │         │
                    └──┬─────┘  └─────────┘
                       │
              ┌────────▼────────┐
              │    MongoDB      │
              │  (StatefulSet)  │
              │  + PVC (5Gi)    │
              └─────────────────┘

Observability Layer:
  Prometheus ← ServiceMonitor ← Backend /metrics
  Grafana    ← Prometheus datasource
  Fluentd    ← /var/log/pods → Elasticsearch
  Alertmanager ← PrometheusRules → PagerDuty/Slack
```

---

## Technology Stack

| Component | Technology | Why |
|-----------|------------|-----|
| Container Orchestration | Kubernetes (minikube) | Industry standard |
| Backend | Node.js + Express | Simple REST API |
| Frontend | React + Nginx | SPA served as static files |
| Database | MongoDB 6.0 | Document store, StatefulSet demo |
| Ingress | NGINX Ingress Controller | Path-based routing, TLS |
| Metrics | Prometheus + Grafana | Pull-based metrics, dashboards |
| Logging | Fluentd + Elasticsearch | DaemonSet log collection |
| Package Manager | Helm | kube-prometheus-stack install |

---

## Quick Start

```bash
# Prerequisites
minikube start --cpus=4 --memory=8192 --disk-size=30g

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable ingress-dns

# Deploy all phases
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f serviceaccount.yaml
kubectl apply -f rbac.yaml
kubectl apply -f mongodb/
kubectl apply -f backend/
kubectl apply -f frontend/
kubectl apply -f ingress.yaml
kubectl apply -f networkpolicy.yaml
kubectl apply -f pdb.yaml

# Install monitoring stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install kube-prometheus-stack \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=admin123

kubectl apply -f backend/servicemonitor.yaml
kubectl apply -f backend/prometheusrule.yaml
kubectl apply -f fluentd/

# Set up local DNS
echo "$(minikube ip)  taskapp.local" | sudo tee -a /etc/hosts

# Verify
kubectl get all -n taskapp
kubectl get all -n monitoring
curl -k https://taskapp.local/api/health
```

---

## File Structure

```
k8s-microservices/
├── README.md                           ← This file
├── namespace.yaml                      ← Namespace + PSA labels
├── configmap.yaml                      ← Non-sensitive app config
├── secret.yaml                         ← DB credentials (base64)
├── serviceaccount.yaml                 ← Per-component service accounts
├── rbac.yaml                           ← Role + RoleBinding
├── ingress.yaml                        ← NGINX Ingress + TLS
├── networkpolicy.yaml                  ← Pod-to-pod network restrictions
├── pdb.yaml                            ← PodDisruptionBudget
├── backend/
│   ├── deployment.yaml                 ← Probes + security context + resources
│   ├── service.yaml                    ← ClusterIP Service (port named "http")
│   ├── hpa.yaml                        ← HPA (CPU + memory scaling)
│   ├── servicemonitor.yaml             ← Prometheus scrape config
│   └── prometheusrule.yaml             ← Alerting rules
├── frontend/
│   ├── deployment.yaml
│   └── service.yaml
├── mongodb/
│   ├── statefulset.yaml                ← volumeClaimTemplates, probes
│   └── service.yaml                    ← Headless (clusterIP: None)
└── fluentd/
    ├── rbac.yaml                       ← ClusterRole for pod/namespace read
    └── daemonset.yaml                  ← One per node, reads /var/log/pods
```

---

## Phase Summary

| Phase | What It Demonstrates | Key Concepts |
|-------|---------------------|--------------|
| **1 - App Deployment** | Core Kubernetes objects | Deployment, StatefulSet, Service, ConfigMap, Secret, PVC |
| **2 - Production Readiness** | Making apps safe to run | Liveness/Readiness/Startup probes, Resource requests/limits, HPA |
| **3 - Networking** | Traffic management | Ingress, TLS, NetworkPolicy, path-based routing |
| **4 - Security** | Hardening workloads | ServiceAccount, RBAC, Pod Security Standards, securityContext |
| **5 - Observability** | Knowing what's happening | Prometheus, Grafana, Fluentd, PromQL, Alerting |
| **6 - Failure Testing** | Proving resilience | CrashLoopBackOff, OOMKill, DB outage, load testing, postmortems |

---

## Interview Cheat Sheet: "Tell Me About This Project"

### 30-Second Pitch
> "I built a production-grade microservices application on Kubernetes covering the full
> lifecycle: from initial deployment with StatefulSets and persistent volumes, through
> production hardening with health probes and HPA, to security hardening with RBAC and
> Pod Security Standards, and observability with Prometheus and Grafana. The most valuable
> part was failure testing — I deliberately broke the MongoDB connection, simulated pod
> kills, injected bad config, and ran load tests with k6. Each scenario taught me exactly
> how Kubernetes detection and recovery works at every layer."

### Questions You'll Be Asked

**Q: Why StatefulSet for MongoDB instead of Deployment?**
> StatefulSets provide: (1) stable, predictable pod names (`mongodb-0`, not a random hash),
> (2) stable network identity via headless service DNS, (3) ordered pod creation/deletion,
> (4) per-pod PersistentVolumeClaims via `volumeClaimTemplates`. Deployments don't guarantee
> any of these — deleting and recreating a Deployment pod could mount a different PVC.

**Q: What happens to in-flight requests during a rolling update?**
> With `maxUnavailable: 0` and a `preStop: sleep 5` hook:
> (1) Kubernetes sends SIGTERM, (2) preStop hook fires and waits 5s (LB drains connection),
> (3) after hook completes, the container gets SIGTERM, (4) `terminationGracePeriodSeconds: 30`
> gives it time to finish in-flight requests before SIGKILL.

**Q: How does HPA know when to scale?**
> HPA queries the metrics-server every 15s (default). When average CPU across all pods
> exceeds the target utilization, it calculates `desiredReplicas = ceil(currentReplicas × (currentMetric / desiredMetric))`.
> `stabilizationWindowSeconds` prevents thrashing by requiring the condition to persist
> before acting.

**Q: Walk me through debugging a CrashLoopBackOff.**
> 1. `kubectl get pods` — identify the pod in CrashLoopBackOff
> 2. `kubectl logs <pod> --previous` — read the crash reason
> 3. `kubectl describe pod <pod>` — check Events section (OOMKill? Probe failure? Image pull error?)
> 4. `kubectl exec -it <pod> -- env` — verify injected config
> 5. `kubectl get events --sort-by=.lastTimestamp` — timeline of what happened

**Q: How do you prevent a bad deployment from taking down production?**
> (1) `maxUnavailable: 0` in RollingUpdate keeps current pods serving until new ones are
> ready. (2) Readiness probes gate traffic — a new pod with bad config fails the probe and
> never receives traffic. (3) `kubectl rollout undo` instantly reverts. (4) PodDisruptionBudget
> ensures a minimum number of pods are always available during voluntary disruptions.

**Q: What's the difference between a Role and ClusterRole?**
> `Role` grants permissions within a single namespace. `ClusterRole` is cluster-scoped
> — it can grant permissions on cluster-level resources (Nodes, PersistentVolumes, Namespaces)
> or be reused across all namespaces via `ClusterRoleBinding`. Always use the narrowest
> scope possible (Role + RoleBinding over ClusterRole + ClusterRoleBinding).

---

## Metrics-Driven SRE Framing

| SLI | Measurement | SLO |
|-----|------------|-----|
| Request success rate | `1 - rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` | ≥ 99.5% |
| P95 latency | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` | ≤ 300ms |
| Pod availability | `kube_deployment_status_replicas_available / kube_deployment_spec_replicas` | ≥ 100% |
| DB connection success | Custom metric from backend | ≥ 99.9% |

---

## Cleanup

```bash
kubectl delete namespace taskapp
kubectl delete namespace monitoring
helm uninstall kube-prometheus-stack -n monitoring
minikube stop
```
-e 

---


# Phase 1: App Deployment

## Project Structure

```
k8s-microservices/
├── namespace.yaml
├── configmap.yaml
├── secret.yaml
├── backend/
│   ├── deployment.yaml
│   └── service.yaml
├── frontend/
│   ├── deployment.yaml
│   └── service.yaml
├── mongodb/
│   ├── statefulset.yaml
│   ├── service.yaml
│   └── pvc.yaml
```

---

## 1. Namespace

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: taskapp
  labels:
    app.kubernetes.io/managed-by: kubectl
    environment: production
```

```bash
kubectl apply -f namespace.yaml
kubectl config set-context --current --namespace=taskapp
```

---

## 2. ConfigMap (non-sensitive config)

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: taskapp
data:
  MONGO_HOST: "mongodb-service"
  MONGO_PORT: "27017"
  MONGO_DB: "taskdb"
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  PORT: "3000"
```

---

## 3. Secret (DB credentials)

```bash
# Generate base64-encoded values
echo -n "admin" | base64          # YWRtaW4=
echo -n "SuperSecret123!" | base64 # U3VwZXJTZWNyZXQxMjMh
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: mongo-secret
  namespace: taskapp
type: Opaque
data:
  MONGO_USERNAME: YWRtaW4=
  MONGO_PASSWORD: U3VwZXJTZWNyZXQxMjMh
  MONGO_URI: bW9uZ29kYjovL2FkbWluOlN1cGVyU2VjcmV0MTIzIUBtb25nb2RiLXNlcnZpY2U6MjcwMTcvdGFza2Ri
```

> **Note:** In production use Sealed Secrets or HashiCorp Vault — never commit raw secrets to Git.

---

## 4. MongoDB StatefulSet + PVC

```yaml
# mongodb/statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
  namespace: taskapp
  labels:
    app: mongodb
    tier: database
spec:
  serviceName: "mongodb-service"
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
        tier: database
    spec:
      containers:
      - name: mongodb
        image: mongo:6.0
        ports:
        - containerPort: 27017
          name: mongo
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: MONGO_USERNAME
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: MONGO_PASSWORD
        - name: MONGO_INITDB_DATABASE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: MONGO_DB
        volumeMounts:
        - name: mongo-data
          mountPath: /data/db
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "500m"
            memory: "1Gi"
  volumeClaimTemplates:
  - metadata:
      name: mongo-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
```

```yaml
# mongodb/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
  namespace: taskapp
  labels:
    app: mongodb
spec:
  selector:
    app: mongodb
  ports:
  - port: 27017
    targetPort: 27017
    name: mongo
  clusterIP: None   # Headless service — required for StatefulSet DNS
```

> **Why StatefulSet?** MongoDB needs stable network identity (`mongodb-0.mongodb-service`),
> persistent storage, and ordered pod management. Deployments don't guarantee this.

---

## 5. Backend API Deployment + Service

```yaml
# backend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: taskapp
  labels:
    app: backend
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        version: v1
    spec:
      containers:
      - name: backend
        image: harshwardhan/task-backend:v1   # Replace with your image
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: PORT
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: NODE_ENV
        - name: MONGO_URI
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: MONGO_URI
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "300m"
            memory: "256Mi"
```

```yaml
# backend/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: taskapp
  labels:
    app: backend
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
  type: ClusterIP
```

---

## 6. Frontend Deployment + Service

```yaml
# frontend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: taskapp
  labels:
    app: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: harshwardhan/task-frontend:v1   # Replace with your image
        ports:
        - containerPort: 80
          name: http
        env:
        - name: REACT_APP_API_URL
          value: "http://taskapp.local/api"
        resources:
          requests:
            cpu: "50m"
            memory: "64Mi"
          limits:
            cpu: "200m"
            memory: "128Mi"
```

```yaml
# frontend/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: taskapp
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

---

## Apply Phase 1

```bash
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f mongodb/
kubectl apply -f backend/
kubectl apply -f frontend/

# Verify
kubectl get all -n taskapp
kubectl get pvc -n taskapp
kubectl describe statefulset mongodb -n taskapp
```

## Verify MongoDB is up before backend starts

```bash
kubectl exec -it mongodb-0 -n taskapp -- mongosh \
  -u admin -p SuperSecret123! --authenticationDatabase admin \
  --eval "db.adminCommand({ ping: 1 })"
```
-e 

---


# Phase 2: Production Readiness

## Liveness, Readiness & Startup Probes

### Why Each Probe Exists

| Probe | What Kubernetes Asks | Action on Failure |
|-------|---------------------|-------------------|
| **Startup** | Has the app finished initializing? | Restart container |
| **Readiness** | Is the app ready to receive traffic? | Remove from Service endpoints |
| **Liveness** | Is the app alive / not deadlocked? | Restart container |

> **Order of execution:** Startup runs FIRST. Only after it succeeds do Liveness and Readiness begin.
> This prevents false restarts during slow app boot (e.g., migration scripts, JVM warmup).

---

## Updated Backend Deployment (Full Production Config)

```yaml
# backend/deployment.yaml (production-ready)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: taskapp
  labels:
    app: backend
    version: v1
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1         # Spin up 1 extra pod during update
      maxUnavailable: 0   # Never take a pod down before a new one is ready
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        version: v1
    spec:
      terminationGracePeriodSeconds: 30   # Give in-flight requests time to finish

      containers:
      - name: backend
        image: harshwardhan/task-backend:v1
        ports:
        - containerPort: 3000
          name: http

        env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: PORT
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: NODE_ENV
        - name: MONGO_URI
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: MONGO_URI

        # ─── Probes ───────────────────────────────────────────────────────────

        startupProbe:
          httpGet:
            path: /healthz
            port: 3000
          failureThreshold: 30    # 30 × 10s = 5 minutes max for startup
          periodSeconds: 10
          # If startup probe doesn't pass in 5 min → container is killed

        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 3
          successThreshold: 1
          timeoutSeconds: 3
          # Pod removed from Service endpoints on 3 consecutive failures

        livenessProbe:
          httpGet:
            path: /healthz
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 20
          failureThreshold: 3
          timeoutSeconds: 5
          # Pod restarted on 3 consecutive failures

        # ─── Resources ────────────────────────────────────────────────────────

        resources:
          requests:
            cpu: "100m"       # Guaranteed CPU — used by scheduler for placement
            memory: "128Mi"   # Guaranteed memory
          limits:
            cpu: "300m"       # Throttled if exceeded (never killed)
            memory: "256Mi"   # Killed with OOMKill if exceeded

        # ─── Lifecycle ────────────────────────────────────────────────────────

        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]
              # Gives load balancer time to route traffic away before SIGTERM
```

---

## Readiness vs Liveness Endpoint (what your backend should expose)

```javascript
// Node.js Express example
const mongoose = require('mongoose');

// Readiness: Is DB connected? (if not, don't send traffic here)
app.get('/ready', async (req, res) => {
  try {
    if (mongoose.connection.readyState !== 1) {
      return res.status(503).json({ status: 'not ready', db: 'disconnected' });
    }
    await mongoose.connection.db.admin().ping();
    res.json({ status: 'ready' });
  } catch (err) {
    res.status(503).json({ status: 'not ready', error: err.message });
  }
});

// Liveness: Is the process itself alive? (minimal check, no external deps)
app.get('/healthz', (req, res) => {
  res.json({ status: 'alive', uptime: process.uptime() });
});
```

---

## HPA — Horizontal Pod Autoscaler (CPU-based)

```yaml
# backend/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: taskapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60   # Scale up when avg CPU > 60%

  # Memory-based scaling (bonus — requires custom metrics adapter in real clusters)
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60    # Wait 60s before scaling up again
      policies:
      - type: Pods
        value: 2                        # Add max 2 pods per scale event
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scaling down (prevent flapping)
      policies:
      - type: Pods
        value: 1
        periodSeconds: 120
```

> **Important:** HPA requires the metrics-server to be installed.
> ```bash
> # For minikube
> minikube addons enable metrics-server
>
> # Verify metrics flow
> kubectl top pods -n taskapp
> kubectl top nodes
> ```

---

## MongoDB Production Readiness

```yaml
# mongodb/statefulset.yaml (production probes added)
# Inside the container spec:

        livenessProbe:
          exec:
            command:
            - mongosh
            - --eval
            - "db.adminCommand({ ping: 1 })"
          initialDelaySeconds: 30
          periodSeconds: 20
          timeoutSeconds: 10
          failureThreshold: 3

        readinessProbe:
          exec:
            command:
            - mongosh
            - --eval
            - "db.adminCommand({ ping: 1 })"
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "500m"
            memory: "1Gi"
```

---

## Apply Phase 2

```bash
kubectl apply -f backend/deployment.yaml
kubectl apply -f backend/hpa.yaml

# Watch HPA
kubectl get hpa -n taskapp -w

# Describe to see current/desired replicas and conditions
kubectl describe hpa backend-hpa -n taskapp

# Watch pods scale
kubectl get pods -n taskapp -w
```

## Key Interview Questions This Covers

**Q: What's the difference between liveness and readiness probes?**
> Readiness controls whether a pod receives traffic. Liveness controls whether the pod is restarted. A pod can be alive but not ready (e.g., still connecting to DB). Kubernetes never sends traffic to an unready pod, but won't restart it either.

**Q: Why use `requests` and `limits`?**
> `requests` are what the scheduler uses to decide which node to place the pod on — it's a *guaranteed* allocation. `limits` are the ceiling — CPU is throttled at the limit, memory causes OOMKill. Setting only limits (no requests) defaults requests to equal limits, which wastes capacity. Setting requests with no limits risks noisy-neighbour problems.

**Q: What happens if HPA and the Deployment's `replicas` conflict?**
> Once HPA takes control, manually setting `replicas` in the Deployment YAML will be overwritten by the HPA on the next sync. Best practice: remove `replicas` from Deployment once HPA is active, or set it equal to `minReplicas`.
-e 

---


# Phase 3: Networking — Ingress + TLS

## Install NGINX Ingress Controller

```bash
# For minikube
minikube addons enable ingress
minikube addons enable ingress-dns

# Verify controller pod is Running
kubectl get pods -n ingress-nginx

# For bare-metal / generic clusters
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml
```

---

## Generate Self-Signed TLS Certificate (for local dev)

```bash
# Create a self-signed cert for taskapp.local
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=taskapp.local/O=TaskApp"

# Store as a Kubernetes Secret
kubectl create secret tls taskapp-tls \
  --cert=tls.crt \
  --key=tls.key \
  -n taskapp

# Verify
kubectl get secret taskapp-tls -n taskapp
kubectl describe secret taskapp-tls -n taskapp
```

---

## Ingress Resource

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: taskapp-ingress
  namespace: taskapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    nginx.ingress.kubernetes.io/rate-limit: "100"          # Requests/min per IP
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - taskapp.local
    secretName: taskapp-tls

  rules:
  - host: taskapp.local
    http:
      paths:

      # Route /api/* → backend service (strip /api prefix via rewrite-target)
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 80

      # Route /* → frontend service
      - path: /()(.*)
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

---

## /etc/hosts Configuration

```bash
# Get the minikube IP
minikube ip
# e.g., 192.168.49.2

# Add to /etc/hosts
echo "192.168.49.2  taskapp.local" | sudo tee -a /etc/hosts

# Test
curl -k https://taskapp.local/api/health
curl -k https://taskapp.local
```

---

## NetworkPolicy — Restrict Traffic Between Pods

```yaml
# networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-netpol
  namespace: taskapp
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress

  ingress:
  # Allow traffic only from ingress controller
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: ingress-nginx
    ports:
    - protocol: TCP
      port: 3000

  egress:
  # Allow backend to reach MongoDB only
  - to:
    - podSelector:
        matchLabels:
          app: mongodb
    ports:
    - protocol: TCP
      port: 27017

  # Allow DNS resolution
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
```

```yaml
# networkpolicy-mongodb.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mongodb-netpol
  namespace: taskapp
spec:
  podSelector:
    matchLabels:
      app: mongodb
  policyTypes:
  - Ingress

  ingress:
  # MongoDB only accepts connections from backend
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 27017
```

---

## Apply Phase 3

```bash
kubectl apply -f ingress.yaml
kubectl apply -f networkpolicy.yaml
kubectl apply -f networkpolicy-mongodb.yaml

# Check Ingress
kubectl get ingress -n taskapp
kubectl describe ingress taskapp-ingress -n taskapp

# Tail Ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx -f
```

---

## Verify End-to-End Routing

```bash
# Full path test
curl -k -v https://taskapp.local/api/health
# Expected: {"status":"ready"} with 200

curl -k -v https://taskapp.local/
# Expected: HTML from frontend

# Test rate limiting
for i in {1..120}; do curl -sk https://taskapp.local/api/health; done
# After 100 requests: 503 or 429 from nginx
```

---

## Interview Deep-Dive: Ingress vs LoadBalancer vs NodePort

| Type | Use Case | External IP | Cost |
|------|----------|-------------|------|
| **ClusterIP** | Internal only | None | Free |
| **NodePort** | Dev/testing | Node IP + port | Free but limited |
| **LoadBalancer** | Cloud production | Cloud LB IP | 💰 per service |
| **Ingress** | Production (multiple services) | 1 shared LB IP | Most efficient |

**Q: Why use Ingress over individual LoadBalancer Services?**
> With 10 microservices, 10 LoadBalancers = 10 cloud LB costs + 10 IPs to manage.
> Ingress provides one entry point, one TLS cert, path-based routing, and one IP — the NGINX controller is the only LoadBalancer service you need.
-e 

---


# Phase 4: Security — RBAC + Pod Security Standards

## Why Security in Kubernetes?

By default, every pod runs as root, has a default ServiceAccount with broad permissions,
and can potentially access the Kubernetes API to enumerate other resources.
This phase locks all of that down.

---

## 1. ServiceAccounts (Principle of Least Privilege)

```yaml
# serviceaccount.yaml
# Each component gets its own identity — never share ServiceAccounts

apiVersion: v1
kind: ServiceAccount
metadata:
  name: backend-sa
  namespace: taskapp
  labels:
    app: backend
automountServiceAccountToken: false   # Don't mount API token unless explicitly needed
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: frontend-sa
  namespace: taskapp
automountServiceAccountToken: false
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mongodb-sa
  namespace: taskapp
automountServiceAccountToken: false
```

---

## 2. RBAC — Role + RoleBinding

```yaml
# rbac.yaml
# Role: defines WHAT actions are allowed on WHICH resources (namespace-scoped)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backend-role
  namespace: taskapp
rules:
  # Backend needs to read its own ConfigMap and Secret at runtime
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["app-config"]
  verbs: ["get", "watch"]

- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["mongo-secret"]
  verbs: ["get"]

  # Backend can read pod info for health checking peers (optional)
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
# RoleBinding: assigns the Role to the ServiceAccount
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backend-rolebinding
  namespace: taskapp
subjects:
- kind: ServiceAccount
  name: backend-sa
  namespace: taskapp
roleRef:
  kind: Role
  apiGroup: rbac.authorization.k8s.io
  name: backend-role
```

```yaml
# MongoDB only needs no API access at all — minimal role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: mongodb-role
  namespace: taskapp
rules: []   # Explicitly empty — zero permissions
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: mongodb-rolebinding
  namespace: taskapp
subjects:
- kind: ServiceAccount
  name: mongodb-sa
  namespace: taskapp
roleRef:
  kind: Role
  apiGroup: rbac.authorization.k8s.io
  name: mongodb-role
```

---

## 3. Attach ServiceAccounts to Deployments/StatefulSets

```yaml
# In backend/deployment.yaml — under spec.template.spec:
      serviceAccountName: backend-sa

# In frontend/deployment.yaml:
      serviceAccountName: frontend-sa

# In mongodb/statefulset.yaml:
      serviceAccountName: mongodb-sa
```

---

## 4. Pod Security Standards

Kubernetes 1.25+ ships Pod Security Admission (PSA) built-in.
Apply it at the namespace level via labels.

```yaml
# Update namespace.yaml to enforce restricted security
apiVersion: v1
kind: Namespace
metadata:
  name: taskapp
  labels:
    # Enforce: pods violating the policy are REJECTED
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    # Audit: violations logged but not blocked (use for migration)
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: latest
    # Warn: violating pods get a warning in kubectl output
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

### What "restricted" requires in your pod specs:

```yaml
# These security fields are REQUIRED for restricted PSA to accept your pod
# Add to every container spec:

        securityContext:
          runAsNonRoot: true             # Cannot run as root (UID 0)
          runAsUser: 1000                # Explicit non-root UID
          runAsGroup: 3000
          allowPrivilegeEscalation: false  # Cannot sudo or setuid
          readOnlyRootFilesystem: true    # Filesystem is immutable
          seccompProfile:
            type: RuntimeDefault          # Use the container runtime's seccomp profile
          capabilities:
            drop:
            - ALL                         # Drop ALL Linux capabilities
            # add: [NET_BIND_SERVICE]     # Only add back what's needed (e.g., port 80)
```

---

## 5. Full Secured Backend Deployment

```yaml
# backend/deployment.yaml (security-hardened)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: taskapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      serviceAccountName: backend-sa
      automountServiceAccountToken: false

      # Pod-level security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000          # Volume ownership — files written as this GID
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: backend
        image: harshwardhan/task-backend:v1
        ports:
        - containerPort: 3000

        # Container-level security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL

        # If your app writes temp files, mount a writable tmpfs volume
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: logs
          mountPath: /app/logs

        env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: PORT
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: NODE_ENV
        - name: MONGO_URI
          valueFrom:
            secretKeyRef:
              name: mongo-secret
              key: MONGO_URI

        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "300m"
            memory: "256Mi"

        startupProbe:
          httpGet:
            path: /healthz
            port: 3000
          failureThreshold: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          periodSeconds: 10
          failureThreshold: 3

        livenessProbe:
          httpGet:
            path: /healthz
            port: 3000
          periodSeconds: 20
          failureThreshold: 3
          initialDelaySeconds: 15

      volumes:
      - name: tmp
        emptyDir: {}
      - name: logs
        emptyDir: {}
```

---

## Apply Phase 4

```bash
kubectl apply -f serviceaccount.yaml
kubectl apply -f rbac.yaml

# Reapply namespace with PSA labels
kubectl apply -f namespace.yaml

# Reapply deployments with security contexts
kubectl apply -f backend/deployment.yaml
kubectl apply -f frontend/deployment.yaml
kubectl apply -f mongodb/statefulset.yaml

# Verify RBAC
kubectl auth can-i get configmaps --as=system:serviceaccount:taskapp:backend-sa -n taskapp
# Expected: yes

kubectl auth can-i delete pods --as=system:serviceaccount:taskapp:backend-sa -n taskapp
# Expected: no

# Check PSA enforcement
kubectl describe namespace taskapp | grep pod-security
```

---

## Interview: RBAC Deep Dive

**Role vs ClusterRole?**
> `Role` = namespace-scoped permissions. `ClusterRole` = cluster-wide (e.g., can read nodes, PVs).
> Use `ClusterRoleBinding` to bind a `ClusterRole` to a ServiceAccount globally.
> Always prefer the most narrow scope.

**Q: How would you audit what permissions a ServiceAccount has?**
```bash
kubectl auth can-i --list --as=system:serviceaccount:taskapp:backend-sa -n taskapp
```

**Q: What's the difference between Pod Security Policy (deprecated) and Pod Security Admission?**
> PSP was a cluster-wide, admission controller approach — complex and hard to manage.
> PSA (1.25+) is simpler: you label namespaces with a security level (privileged, baseline, restricted).
> PSA is built-in, no extra admission webhook needed. PSP was removed in 1.25.
-e 

---


# Phase 5: Observability — Prometheus + Grafana + Fluentd

## The Three Pillars of Observability

| Pillar | Tool | What It Tells You |
|--------|------|-------------------|
| **Metrics** | Prometheus + Grafana | System health: CPU, memory, RPS, latency |
| **Logs** | Fluentd + Elasticsearch/Loki | What happened and why |
| **Traces** | Jaeger / OpenTelemetry | Where time is spent across services |

---

## 1. Install kube-prometheus-stack (Prometheus + Grafana + Alertmanager)

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install to monitoring namespace
kubectl create namespace monitoring

helm install kube-prometheus-stack \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=admin123 \
  --set prometheus.prometheusSpec.retention=7d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=10Gi

# Verify all components are up
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

---

## 2. Expose Prometheus Metrics from Your Backend

Your backend must expose a `/metrics` endpoint in Prometheus format.

```javascript
// Node.js — add prom-client
// npm install prom-client

const client = require('prom-client');
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ timeout: 5000 });  // CPU, memory, event loop lag, etc.

// Custom metrics
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5]
});

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

// Middleware to track all requests
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    const labels = { method: req.method, route: req.path, status_code: res.statusCode };
    end(labels);
    httpRequestsTotal.inc(labels);
  });
  next();
});

// Metrics endpoint — Prometheus scrapes this
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

---

## 3. ServiceMonitor — Tell Prometheus to Scrape Your Backend

```yaml
# backend/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend-monitor
  namespace: taskapp
  labels:
    # Must match the prometheus operator's serviceMonitorSelector
    release: kube-prometheus-stack
spec:
  selector:
    matchLabels:
      app: backend
  endpoints:
  - port: http
    path: /metrics
    interval: 30s       # Scrape every 30 seconds
    scrapeTimeout: 10s
  namespaceSelector:
    matchNames:
    - taskapp
```

```yaml
# Update backend/service.yaml to name the port:
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 3000
    name: http        # Must match ServiceMonitor port name
```

---

## 4. PrometheusRule — Alerting

```yaml
# backend/prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: backend-alerts
  namespace: taskapp
  labels:
    release: kube-prometheus-stack
spec:
  groups:
  - name: backend.rules
    interval: 30s
    rules:

    # Alert when pod is down
    - alert: BackendPodDown
      expr: up{job="backend"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Backend pod {{ $labels.pod }} is down"
        description: "Backend pod has been down for more than 1 minute."

    # Alert when error rate > 5%
    - alert: HighErrorRate
      expr: |
        rate(http_requests_total{status_code=~"5.."}[5m])
        /
        rate(http_requests_total[5m]) > 0.05
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "High HTTP error rate on backend"
        description: "Error rate is {{ $value | humanizePercentage }}"

    # Alert when P99 latency > 1 second
    - alert: HighLatency
      expr: |
        histogram_quantile(0.99,
          rate(http_request_duration_seconds_bucket[5m])
        ) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "P99 latency above 1s"
        description: "99th percentile latency: {{ $value }}s"

    # Alert when memory > 80% of limit
    - alert: HighMemoryUsage
      expr: |
        container_memory_usage_bytes{namespace="taskapp", container="backend"}
        /
        container_spec_memory_limit_bytes{namespace="taskapp", container="backend"} > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Backend memory usage above 80%"
```

---

## 5. Access Grafana

```bash
# Port-forward Grafana (or add to Ingress)
kubectl port-forward svc/kube-prometheus-stack-grafana -n monitoring 3000:80

# Open http://localhost:3000
# Username: admin
# Password: admin123
```

### Useful Grafana Dashboards to Import

| Dashboard ID | Name |
|-------------|------|
| `3119` | Kubernetes cluster monitoring |
| `6417` | Kubernetes pods |
| `13770` | Node Exporter Full |
| `11074` | Node.js application |
| `7249` | MongoDB |

```bash
# Grafana dashboard import: Dashboards → Import → Enter ID → Load
```

---

## 6. Fluentd — Log Collection

```yaml
# fluentd/daemonset.yaml
# Fluentd runs as a DaemonSet — one pod per node, reads all container logs
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: monitoring
  labels:
    app: fluentd
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      serviceAccountName: fluentd-sa
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule

      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch-service"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        - name: FLUENT_ELASTICSEARCH_SCHEME
          value: "http"
        - name: FLUENT_CONTAINER_TAIL_EXCLUDE_PATH
          value: "/var/log/containers/fluentd*"

        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi

        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: dockercontainerlogdirectory
          mountPath: /var/log/pods
          readOnly: true

      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: dockercontainerlogdirectory
        hostPath:
          path: /var/log/pods
```

### Fluentd RBAC (needs to read pod/namespace metadata)

```yaml
# fluentd/rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentd-sa
  namespace: monitoring
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fluentd-role
rules:
- apiGroups: [""]
  resources: ["pods", "namespaces"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fluentd-rolebinding
roleRef:
  kind: ClusterRole
  name: fluentd-role
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: fluentd-sa
  namespace: monitoring
```

---

## 7. Structured Logging from Backend

Fluentd parses JSON logs automatically. Configure your backend to emit structured JSON:

```javascript
// Winston structured logger for Node.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()]
});

// Usage
logger.info('Request received', {
  method: req.method,
  path: req.path,
  userId: req.user?.id,
  requestId: req.headers['x-request-id']
});

logger.error('MongoDB connection failed', {
  error: err.message,
  stack: err.stack,
  mongoHost: process.env.MONGO_HOST
});
```

This produces:
```json
{"level":"info","message":"Request received","method":"GET","path":"/api/tasks","timestamp":"2024-01-15T10:30:00.000Z"}
```

---

## Apply Phase 5

```bash
kubectl apply -f backend/servicemonitor.yaml
kubectl apply -f backend/prometheusrule.yaml
kubectl apply -f fluentd/rbac.yaml
kubectl apply -f fluentd/daemonset.yaml

# Verify Prometheus is scraping your service
# In Prometheus UI (port-forward to :9090)
# Go to Status → Targets → look for taskapp/backend
kubectl port-forward svc/kube-prometheus-stack-prometheus -n monitoring 9090:9090

# Check alert rules loaded
# Prometheus UI → Alerts
```

---

## Key PromQL Queries to Know

```promql
# Request rate (RPS) for backend
rate(http_requests_total{namespace="taskapp"}[5m])

# Error rate percentage
rate(http_requests_total{status_code=~"5..",namespace="taskapp"}[5m])
/ rate(http_requests_total{namespace="taskapp"}[5m]) * 100

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{namespace="taskapp"}[5m]))

# Memory usage vs limit
container_memory_usage_bytes{namespace="taskapp"}
/ container_spec_memory_limit_bytes{namespace="taskapp"} * 100

# Pod restarts in last hour
increase(kube_pod_container_status_restarts_total{namespace="taskapp"}[1h])

# CPU throttling ratio (important for tuning limits)
rate(container_cpu_throttled_seconds_total{namespace="taskapp"}[5m])
/ rate(container_cpu_usage_seconds_total{namespace="taskapp"}[5m])
```
-e 

---


# Phase 6: Failure Testing — Break It to Understand It

> This is the most important phase for interviews. When you say "I tested failure scenarios
> and documented the blast radius," you immediately stand out from candidates who only deployed.

---

## Scenario 1: Pod Kill (Self-Healing Test)

### What to Simulate
```bash
# Delete a backend pod directly
kubectl delete pod -l app=backend -n taskapp --wait=false

# Or kill a specific pod by name
kubectl get pods -n taskapp
kubectl delete pod backend-7d6b9f7c4-xk9p2 -n taskapp
```

### What to Watch
```bash
# Watch pods recover in real time
kubectl get pods -n taskapp -w

# Expected output:
# backend-7d6b9f7c4-xk9p2   Terminating   0   2m
# backend-7d6b9f7c4-m7n3p   ContainerCreating   0   0s
# backend-7d6b9f7c4-m7n3p   Running   0   8s
```

### Debug Steps
```bash
kubectl describe pod <new-pod-name> -n taskapp   # Check events
kubectl logs <pod-name> -n taskapp --previous    # Logs from crashed container
kubectl get events -n taskapp --sort-by='.lastTimestamp'
```

### Documentation

| Field | Detail |
|-------|--------|
| **Scenario** | Pod killed manually (simulates node failure, OOMKill, crash) |
| **Detection** | Kubernetes ReplicaSet controller detects actual < desired replicas |
| **Recovery Time** | ~8–15 seconds (image pull cache hit) |
| **Impact** | Readiness probe gates traffic — zero user-facing errors during recovery |
| **Root Cause** | N/A (forced failure) |
| **Fix** | Kubernetes self-heals automatically. Prevention: set PodDisruptionBudget |
| **Prevention** | `minAvailable: 1` in PodDisruptionBudget ensures ≥1 pod always running |

### PodDisruptionBudget

```yaml
# pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: backend-pdb
  namespace: taskapp
spec:
  minAvailable: 1   # At least 1 backend pod must always be Running
  selector:
    matchLabels:
      app: backend
```

```bash
kubectl apply -f pdb.yaml

# Now try to drain a node — PDB will block if it would violate the budget
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
```

---

## Scenario 2: Database Connection Break

### Simulate — Wrong MongoDB Service Name

```bash
# Temporarily patch the MONGO_URI secret with a wrong hostname
kubectl patch secret mongo-secret -n taskapp \
  --type='json' \
  -p='[{"op":"replace","path":"/data/MONGO_URI","value":"bW9uZ29kYjovL2FkbWluOlN1cGVyU2VjcmV0MTIzIUB3cm9uZy1ob3N0OjI3MDE3L3Rhc2tkYg=="}]'
# (base64 of "mongodb://admin:SuperSecret123!@wrong-host:27017/taskdb")

# Force a rolling restart to pick up the new secret
kubectl rollout restart deployment/backend -n taskapp
```

### What to Observe
```bash
# Watch the readiness probe fail
kubectl get pods -n taskapp -w

# The pod will show READY = 0/1 because /ready returns 503
# Kubernetes removes it from Service endpoints
# All traffic routes to the remaining healthy pod

# Check what's happening
kubectl logs <backend-pod> -n taskapp
# Expected: MongoNetworkError: connection refused / ENOTFOUND wrong-host

kubectl describe pod <backend-pod> -n taskapp
# Events: Readiness probe failed: ...
```

### Debug Steps

```bash
# Step 1: Check pod status
kubectl get pods -n taskapp

# Step 2: Look at events
kubectl get events -n taskapp --field-selector reason=Unhealthy

# Step 3: Check readiness endpoint manually
kubectl exec -it <backend-pod> -n taskapp -- curl localhost:3000/ready
# Returns: {"status":"not ready","db":"disconnected"}

# Step 4: Test DNS resolution from inside the pod
kubectl exec -it <backend-pod> -n taskapp -- nslookup mongodb-service
kubectl exec -it <backend-pod> -n taskapp -- nc -zv mongodb-service 27017

# Step 5: Verify the secret value
kubectl get secret mongo-secret -n taskapp -o jsonpath='{.data.MONGO_URI}' | base64 -d

# Step 6: Fix the secret
kubectl patch secret mongo-secret -n taskapp \
  --type='json' \
  -p='[{"op":"replace","path":"/data/MONGO_URI","value":"bW9uZ29kYjovL2FkbWluOlN1cGVyU2VjcmV0MTIzIUBtb25nb2RiLXNlcnZpY2U6MjcwMTcvdGFza2Ri"}]'

kubectl rollout restart deployment/backend -n taskapp
kubectl rollout status deployment/backend -n taskapp
```

### Documentation

| Field | Detail |
|-------|--------|
| **Scenario** | Backend cannot connect to MongoDB (wrong hostname in MONGO_URI) |
| **Detection** | `/ready` endpoint returns 503 → pod removed from Service endpoints |
| **User Impact** | Zero — remaining pods handled traffic; HPA would scale if needed |
| **Detection Method** | `kubectl get events -n taskapp` showed repeated Unhealthy events |
| **Root Cause** | Secret contained wrong MongoDB hostname after misconfigured patch |
| **Fix** | Corrected MONGO_URI in secret + rollout restart |
| **MTTR** | 4 minutes (detection: 30s, diagnosis: 2m, fix: 1.5m) |
| **Prevention** | Validate secrets in CI/CD pipeline before applying; use external secret manager (Vault) with validation |

---

## Scenario 3: Wrong ConfigMap (Bad Configuration)

### Simulate — Invalid PORT Value

```bash
# Set an invalid port in ConfigMap
kubectl patch configmap app-config -n taskapp \
  --type merge \
  -p '{"data":{"PORT":"invalid-port"}}'

kubectl rollout restart deployment/backend -n taskapp
```

### What to Observe
```bash
kubectl get pods -n taskapp -w
# Pod enters CrashLoopBackOff — app crashes on startup trying to listen on "invalid-port"

kubectl logs <crashloopbackoff-pod> -n taskapp
# Error: listen EADDRNOTAVAIL: address not available invalid-port:invalid-port

kubectl describe pod <crashloopbackoff-pod> -n taskapp
# Events: Back-off restarting failed container
```

### Debug Steps

```bash
# Step 1: Check pod status - CrashLoopBackOff is the smoking gun
kubectl get pods -n taskapp

# Step 2: Read the error — logs from previous crash
kubectl logs <pod> -n taskapp --previous

# Step 3: Verify what config was injected into the pod
kubectl exec -it <running-pod> -n taskapp -- env | grep PORT

# Step 4: Check the ConfigMap directly
kubectl get configmap app-config -n taskapp -o yaml

# Step 5: Fix the ConfigMap
kubectl patch configmap app-config -n taskapp \
  --type merge \
  -p '{"data":{"PORT":"3000"}}'

kubectl rollout restart deployment/backend -n taskapp
kubectl rollout status deployment/backend -n taskapp
```

### Rollback with kubectl

```bash
# If a new deployment is broken, rollback immediately
kubectl rollout undo deployment/backend -n taskapp

# Or rollback to a specific revision
kubectl rollout history deployment/backend -n taskapp
kubectl rollout undo deployment/backend -n taskapp --to-revision=2
```

### Documentation

| Field | Detail |
|-------|--------|
| **Scenario** | Bad ConfigMap value causes app crash on startup |
| **Symptom** | CrashLoopBackOff — exponential back-off (10s, 20s, 40s, 80s...) |
| **Impact** | Only new pods affected; existing running pods continue serving traffic (RollingUpdate kept 1 pod alive) |
| **Detection** | `kubectl get pods` showed CrashLoopBackOff; `kubectl logs --previous` showed error |
| **Root Cause** | `PORT=invalid-port` injected via ConfigMap patch |
| **Fix** | Corrected ConfigMap + rollout restart |
| **Prevention** | ConfigMap schema validation in CI; use `kubectl diff` before applying; Admission Webhooks to validate config values |

---

## Scenario 4: High Load / CPU Spike (HPA Trigger)

### Simulate Load with k6

```bash
# Install k6
brew install k6  # or: sudo apt install k6

# Create load test script
cat <<EOF > load-test.js
import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 20 },   // Ramp up to 20 VUs
    { duration: '3m', target: 50 },   // Hold at 50 VUs (should trigger HPA)
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  }
};

export default function() {
  http.get('https://taskapp.local/api/tasks', {
    headers: { 'Content-Type': 'application/json' }
  });
  sleep(0.5);
}
EOF

k6 run --insecure-skip-tls-verify load-test.js
```

### Watch HPA Respond

```bash
# In a separate terminal — watch HPA scale
watch kubectl get hpa backend-hpa -n taskapp

# Watch pods being added
kubectl get pods -n taskapp -w

# Watch CPU metrics in real time
watch kubectl top pods -n taskapp
```

### Expected Output Progression

```
NAME          REFERENCE             TARGETS   MINPODS   MAXPODS   REPLICAS
backend-hpa   Deployment/backend    68%/60%   2         10        2
backend-hpa   Deployment/backend    74%/60%   2         10        4    ← scaling up
backend-hpa   Deployment/backend    55%/60%   2         10        4
backend-hpa   Deployment/backend    48%/60%   2         10        4    ← stabilizing
backend-hpa   Deployment/backend    12%/60%   2         10        2    ← scaling down (after 5m)
```

### Documentation

| Field | Detail |
|-------|--------|
| **Scenario** | Simulated 50 concurrent users via k6 load test |
| **Trigger** | CPU average exceeded 60% threshold (HPA configured) |
| **Scale-up Time** | ~60 seconds (stabilizationWindow) |
| **Scale-down Time** | ~5 minutes (stabilizationWindowSeconds: 300 prevents flapping) |
| **User Impact** | P95 latency stayed under 300ms due to auto-scaling |
| **Bottleneck Found** | MongoDB became the bottleneck at 8 replicas — connection pool exhausted |
| **Fix** | Added MongoDB connection pooling limits in backend; tuned `maxPoolSize` |
| **Follow-up** | Added MongoDB `PrometheusRule` alert for connection pool saturation |

---

## Scenario 5: Node Failure Simulation

```bash
# Cordon node (mark unschedulable — simulate node going down)
kubectl cordon minikube

# Drain (evict all pods from node)
kubectl drain minikube --ignore-daemonsets --delete-emptydir-data --force

# Watch pods reschedule
kubectl get pods -n taskapp -w

# Uncordon when done
kubectl uncordon minikube
```

---

## Incident Report Template (Blameless Postmortem)

```markdown
## Incident Report: [IR-001] MongoDB Connection Break

**Date:** 2024-01-15
**Severity:** SEV-2 (Degraded, no complete outage)
**Duration:** 4 minutes 32 seconds
**Author:** [Your Name]

### Summary
A misconfigured MONGO_URI secret caused newly rolled-out backend pods to fail
their readiness probe. Traffic was routed to remaining healthy pods. No user requests
were dropped.

### Timeline
- 14:03:00 — `kubectl patch secret` applied with incorrect MONGO_URI
- 14:03:05 — Rollout restart triggered
- 14:03:20 — New pods entered Running state but READY = 0/1
- 14:03:25 — Kubernetes removed unready pods from Service endpoints
- 14:04:00 — `kubectl get events` showed repeated Unhealthy events (detected)
- 14:05:30 — Root cause identified: wrong hostname in MONGO_URI
- 14:06:45 — Secret corrected, rollout restarted
- 14:07:32 — All pods READY = 1/1 (resolved)

### Root Cause
Manual `kubectl patch` applied base64 of wrong hostname.
No validation step existed in the workflow.

### Impact
- Backend replicas temporarily reduced from 2 to 1
- No user-visible errors (readiness probe protected traffic)
- HPA did not trigger (existing pod handled load)

### Resolution
Corrected MONGO_URI in the secret to point to the correct headless service DNS name.

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Add secret validation script to CI/CD pipeline | Platform team | 2024-01-22 |
| Implement Vault for secret management | Security team | 2024-02-01 |
| Add Prometheus alert for pod readiness ratio < 50% | SRE team | 2024-01-18 |
| Document secret rotation runbook | On-call team | 2024-01-19 |

### What Went Well
- Readiness probe immediately isolated the failing pod
- The issue was detected via events within 35 seconds
- No user impact thanks to rolling update strategy

### What Went Wrong
- No validation of secret values before applying
- Manual patching without peer review

### Lessons Learned
Never patch secrets manually in production without validation. All secret changes
should go through a versioned, reviewed pipeline.
```

---

## Full Debug Toolkit Reference

```bash
# ─── Pod Inspection ──────────────────────────────────────────────────────────
kubectl get pods -n taskapp -o wide           # Node placement, IP, restarts
kubectl describe pod <pod> -n taskapp         # Events, probe results, resource usage
kubectl logs <pod> -n taskapp                 # Current logs
kubectl logs <pod> -n taskapp --previous      # Logs from last crash
kubectl logs <pod> -n taskapp -c <container>  # Multi-container pod
kubectl logs -l app=backend -n taskapp        # Logs from all backend pods

# ─── Exec Into Pod ───────────────────────────────────────────────────────────
kubectl exec -it <pod> -n taskapp -- /bin/sh
kubectl exec -it <pod> -n taskapp -- curl localhost:3000/ready
kubectl exec -it <pod> -n taskapp -- nslookup mongodb-service
kubectl exec -it <pod> -n taskapp -- nc -zv mongodb-service 27017
kubectl exec -it <pod> -n taskapp -- env | grep MONGO

# ─── Deployment Status ───────────────────────────────────────────────────────
kubectl rollout status deployment/backend -n taskapp
kubectl rollout history deployment/backend -n taskapp
kubectl rollout undo deployment/backend -n taskapp

# ─── Resource Usage ──────────────────────────────────────────────────────────
kubectl top pods -n taskapp
kubectl top nodes
kubectl describe node minikube | grep -A 20 "Allocated resources"

# ─── Events (chronological) ──────────────────────────────────────────────────
kubectl get events -n taskapp --sort-by='.lastTimestamp'
kubectl get events -n taskapp --field-selector reason=OOMKilling
kubectl get events -n taskapp --field-selector reason=BackOff

# ─── Network Debugging ───────────────────────────────────────────────────────
kubectl get endpoints -n taskapp              # Which pod IPs are in each Service
kubectl get ingress -n taskapp -o yaml
kubectl describe ingress taskapp-ingress -n taskapp

# ─── StatefulSet Debugging ───────────────────────────────────────────────────
kubectl get statefulset -n taskapp
kubectl describe statefulset mongodb -n taskapp
kubectl get pvc -n taskapp
kubectl describe pvc mongo-data-mongodb-0 -n taskapp
```
