-------------------------------------------------------------------

# 🔹 KUBERNETES TOPICS + FREE LEARNING RESOURCES

*(DevOps interview focused, production mindset)*

---

## 1️⃣ Kubernetes Fundamentals (Must-know baseline)

### Topics

* Kubernetes architecture (control plane, worker nodes)
* Pods & containers
* Namespaces
* Labels & selectors
* kubectl basics

### Free Resources

🎥 **TechWorld with Nana**

* *Kubernetes Architecture Explained*
* *Kubernetes Components Explained*

🎥 **freeCodeCamp – Kubernetes Full Course**

* Watch **Architecture + Core concepts only**

📘 **Official Docs**

* Kubernetes Concepts → Architecture

---

## 2️⃣ Workload Objects (VERY Important for Interviews)

### Topics

* Pod lifecycle
* Deployments
* ReplicaSets
* StatefulSets (when & why)
* DaemonSets
* Jobs & CronJobs
* Rolling updates & rollbacks

### Free Resources

🎥 **TechWorld with Nana**

* *Kubernetes Deployment vs StatefulSet*
* *DaemonSet & Jobs explained*

🎥 **KodeKloud**

* *Kubernetes Workloads Explained*

📘 **Official Docs**

* Workloads → Controllers

---

## 3️⃣ Kubernetes Networking (High-frequency interview area)

### Topics

* Services (ClusterIP, NodePort, LoadBalancer)
* kube-proxy
* DNS in Kubernetes
* Ingress vs Ingress Controller
* Network Policies

### Free Resources

🎥 **TechWorld with Nana**

* *Kubernetes Services Explained*
* *Ingress vs LoadBalancer*

🎥 **That DevOps Guy**

* *Kubernetes Networking Deep Dive*

📘 **Official Docs**

* Concepts → Services & Networking

---

## 4️⃣ Configuration & Secrets Management

### Topics

* ConfigMaps
* Secrets (types, encoding)
* Environment variables vs volumes
* Secret management best practices

### Free Resources

🎥 **TechWorld with Nana**

* *ConfigMaps & Secrets Explained*

🎥 **KodeKloud**

* *Kubernetes Secrets Explained*

📘 **Official Docs**

* Configuration → ConfigMaps & Secrets

---

## 5️⃣ Scaling, Reliability & Availability (SRE Strength Area)

### Topics

* Resource requests & limits
* OOMKill & CPU throttling
* HPA (Horizontal Pod Autoscaler)
* VPA basics
* Pod Disruption Budget (PDB)
* Node failures & pod rescheduling

### Free Resources

🎥 **TechWorld with Nana**

* *Kubernetes Autoscaling Explained*

🎥 **KodeKloud**

* *HPA Deep Dive*
* *Requests vs Limits*

📘 **Official Docs**

* Scaling → HPA

---

## 6️⃣ Health Checks & Probes (Asked a LOT)

### Topics

* Liveness probe
* Readiness probe
* Startup probe
* Real production use cases

### Free Resources

🎥 **TechWorld with Nana**

* *Kubernetes Probes Explained*

🎥 **KodeKloud**

* *Health Checks in Kubernetes*

---

## 7️⃣ Observability & Monitoring (DevOps + SRE Combo)

### Topics

* Metrics vs logs vs traces
* Prometheus architecture
* Alertmanager basics
* Logging (EFK / Loki)
* SLIs & SLOs in Kubernetes

### Free Resources

🎥 **That DevOps Guy**

* *Kubernetes Monitoring Explained*

🎥 **Prometheus Official Channel**

* *Prometheus Kubernetes Monitoring*

📘 **Prometheus Docs**

* Kubernetes integration section

---

## 8️⃣ Kubernetes Security (Hot Interview Topic 🔥)

### Topics

* RBAC (Roles, ClusterRoles, Bindings)
* Service Accounts
* Pod Security Standards (PSS)
* Image security & scanning
* Secrets encryption

### Free Resources

🎥 **TechWorld with Nana**

* *Kubernetes RBAC Explained*

🎥 **KodeKloud**

* *Kubernetes Security Basics*

📘 **Official Docs**

* Security → RBAC & Pod Security

---

## 9️⃣ Helm & Kubernetes Package Management (MANDATORY)

### Topics

* Helm architecture
* Charts & templates
* values.yaml
* Helm vs Kustomize
* Upgrade & rollback

### Free Resources

🎥 **TechWorld with Nana**

* *Helm Explained*

🎥 **freeCodeCamp**

* *Helm Tutorial for Beginners*

📘 **Helm Official Docs**

* Chart development section

---

## 🔟 CI/CD & GitOps with Kubernetes (DevOps Core)

### Topics

* CI/CD pipeline flow
* Blue-Green deployment
* Canary deployment
* GitOps concepts
* ArgoCD basics

### Free Resources

🎥 **That DevOps Guy**

* *GitOps with ArgoCD*

🎥 **TechWorld with Nana**

* *ArgoCD Explained*

📘 **ArgoCD Docs**

* Getting Started

---

## 1️⃣1️⃣ Cloud Kubernetes (AWS EKS – High Demand)

### Topics

* EKS architecture
* IAM Roles for Service Accounts (IRSA)
* Load Balancer Controller
* Node groups & auto scaling
* Cluster upgrades

### Free Resources

🎥 **AWS Official**

* *Amazon EKS Deep Dive*

🎥 **freeCodeCamp**

* *AWS EKS Full Course*

📘 **AWS Docs**

* EKS User Guide

---

## 1️⃣2️⃣ Troubleshooting & Debugging (Interview Killer Skill)

### Topics

* Pod crash loops
* Image pull issues
* DNS failures
* Network issues
* etcd basics & backups

### Free Resources

🎥 **Bret Fisher**

* *Kubernetes Troubleshooting*

🎥 **KodeKloud**

* *Kubernetes Debugging Scenarios*

📘 **Official Docs**

* Troubleshooting section

-------------------------------------------------------------------------------

For **each topic**:

* **Watch 1 primary video**
* **Use the second video only if:**

  * the concept isn’t clear
  * you want production/interview depth
  * you need troubleshooting perspective

Think of it as:

> **Learn once → reinforce only if needed**

---

## 🧭 Which ONE should you choose?

Here’s the **decision guide**, tuned to your profile.

---

## 1️⃣ If the topic is NEW or fuzzy

👉 **Start with TechWorld with Nana**

Why:

* Clear mental models
* Explains *why* things exist
* Fast clarity

Examples:

* Ingress vs LoadBalancer
* Helm
* GitOps
* RBAC

✅ Watch **only Nana first**
⛔ Skip the second video unless confused

---

## 2️⃣ If the topic is OPERATIONAL / TROUBLESHOOTING

👉 **Start with KodeKloud or Bret Fisher**

Why:

* Scenario-based
* Matches interview questions
* Very SRE-friendly

Examples:

* HPA
* Requests vs limits
* Pod crashes
* Debugging

✅ Nana optional
✅ KodeKloud preferred

---

## 3️⃣ If the topic is CI/CD or DevOps workflows

👉 **Start with That DevOps Guy**

Why:

* Real-world pipelines
* Less theory, more “how teams do it”
* Strong DevOps signal in interviews

Examples:

* GitOps
* ArgoCD
* Deployment strategies

✅ One video is enough

---

## 4️⃣ Official Docs — WHEN and HOW to use them (Important)

❌ Don’t read docs like a book
✅ Use docs **selectively**

### Use docs to:

* Confirm syntax
* Understand flags/options
* Reference best practices
* Prepare interview answers

Best approach:

> Video first → Docs for validation

---

## 🧠 Smart Learning Matrix (Very Practical)

| Topic Type            | Watch 1 Video | Watch 2nd Video? |
| --------------------- | ------------- | ---------------- |
| Core concepts         | Yes           | ❌ No             |
| Architecture          | Yes           | ❌ No             |
| Troubleshooting       | Yes           | ✅ If needed      |
| Scaling & reliability | Yes           | ✅ Recommended    |
| Security              | Yes           | ✅ If unclear     |
| CI/CD & GitOps        | Yes           | ❌ No             |
| Cloud (EKS)           | Yes           | ❌ No             |

---

## ⏱️ Time-Optimized Plan (Busy Professional Mode)

* **1 topic/day**
* **30–45 min video**
* **15 min docs**
* **10 min kubectl practice (if possible)**

That’s it. No marathon sessions.

---

## 🎯 Interview Reality Check

Interviewers care about:

* *How* you think
* *How* you troubleshoot
* *How* you protect production

They **do NOT care** how many videos you watched.

If you say:

> “In production, I’d combine HPA with proper requests/limits and PDBs…”

You’ve already passed half the Kubernetes round.

---

### Want me to:

* 🔥 Mark **“must-watch” vs “optional” videos topic-by-topic**
* 🧪 Create **hands-on lab tasks per topic**
* 🧠 Give **interview answer templates** (STAR-style)

Say the word — we’ll optimize this even further 🚀

