# Kubernetes Notes API

A containerized Flask REST API deployed on Kubernetes.

This project was built to practice core Kubernetes and DevOps concepts including Deployments, ReplicaSets, Services, Horizontal Pod Autoscaling, ConfigMaps, Secrets, CronJobs, and health probes.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │       Client        │
                    │  Postman / Browser  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Kubernetes Service  │
                    │      NodePort       │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          ┌──────────┐   ┌──────────┐   ┌──────────┐
          │   Pod    │   │   Pod    │   │   Pod    │
          │ Flask API│   │ Flask API│   │ Flask API│
          └──────────┘   └──────────┘   └──────────┘
                │              │              │
                └──────────────┼──────────────┘
                               │
                        Kubernetes
                        Deployment
                               │
                               ▼
                        Horizontal Pod
                        Autoscaler
                         (2 - 6 Pods)


       ┌─────────────────┐       ┌─────────────────┐
       │    ConfigMap    │       │     Secret      │
       │                 │       │                 │
       │ APP_ENV         │       │ API_KEY         │
       │ LOG_LEVEL       │       │ DB_PASSWORD     │
       │ APP_VERSION     │       │                 │
       └─────────────────┘       └─────────────────┘

                         ┌──────────────┐
                         │   CronJob    │
                         │              │
                         │ Every minute │
                         └──────────────┘
```

---

## Project Structure

```text
k8s-notes-api/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── notes.json
│   └── Dockerfile
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── cronjob.yaml
│
├── README.md
└── .gitignore
```

---

# Technologies

* Python
* Flask
* Docker
* Kubernetes
* Minikube
* kubectl
* Docker Hub
* YAML
* Postman

---

# Kubernetes Concepts Practiced

This project demonstrates:

* Pods
* Deployments
* ReplicaSets
* Rolling updates
* Services
* NodePort
* Horizontal Pod Autoscaler
* ConfigMaps
* Secrets
* CronJobs
* Liveness probes
* Readiness probes
* Environment variables
* Kubernetes self-healing
* Container image deployment

---

# Application

The application is a simple Flask Notes API.

## API Endpoints

| Method | Endpoint      | Description                |
| ------ | ------------- | -------------------------- |
| GET    | `/`           | Application health check   |
| GET    | `/notes`      | Get all notes              |
| POST   | `/notes`      | Create a note              |
| GET    | `/notes/<id>` | Get a specific note        |
| GET    | `/health`     | Kubernetes health endpoint |

---

# Prerequisites

Install the following:

* Docker
* kubectl
* Minikube
* Postman (optional, for API testing)

Verify the installations:

```bash
docker --version
kubectl version --client
minikube version
```

---

# 1. Start Kubernetes

Start Minikube:

```bash
minikube start
```

Verify the cluster:

```bash
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           AGE
minikube   Ready    control-plane   ...
```

---

# 2. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Enter the project directory:

```bash
cd k8s-notes-api
```

---

# 3. Build the Docker Image

Navigate to the application directory:

```bash
cd app
```

Build the image:

```bash
docker build -t <DOCKERHUB_USERNAME>/k8s-notes-api:v2 .
```

Example:

```bash
docker build -t saifkbishi/k8s-notes-api:v2 .
```

Verify the image:

```bash
docker images
```

---

# 4. Push the Image to Docker Hub

Login to Docker Hub:

```bash
docker login
```

Push the image:

```bash
docker push <DOCKERHUB_USERNAME>/k8s-notes-api:v2
```

Example:

```bash
docker push saifkbishi/k8s-notes-api:v2
```

---

# 5. Configure Kubernetes

Return to the project root:

```bash
cd ..
```

Create the Kubernetes namespace: 
## I used the default namespace in this project

```bash
kubectl apply -f k8s/namespace.yaml
```

Verify:

```bash
kubectl get namespaces
```

---

# 6. Create ConfigMap

Apply the ConfigMap:

```bash
kubectl apply -f k8s/configmap.yaml
```

Verify:

```bash
kubectl get configmaps
```

View the configuration:

```bash
kubectl describe configmap notes-api-config
```

---

# 7. Create Secret

Apply the Secret:

```bash
kubectl apply -f k8s/secret.yaml
```

Verify:

```bash
kubectl get secrets
```

To inspect the Secret metadata:

```bash
kubectl describe secret notes-api-secret
```

> Secrets should not be committed to GitHub with real credentials.

For a real project, use a secret-management solution such as Kubernetes Secrets with appropriate RBAC, or an external secret manager.

---

# 8. Deploy the Application

Apply the Deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

Check the Deployment:

```bash
kubectl get deployments
```

Check the ReplicaSet:

```bash
kubectl get replicasets
```

Check the Pods:

```bash
kubectl get pods
```

Expected result:

```text
NAME                         READY   STATUS    RESTARTS
notes-api-xxxxxxxxxx-xxxxx   1/1     Running   0
notes-api-xxxxxxxxxx-yyyyy   1/1     Running   0
notes-api-xxxxxxxxxx-zzzzz   1/1     Running   0
```

The Deployment starts with **3 replicas**.

---

# 9. Expose the Application

Apply the Service:

```bash
kubectl apply -f k8s/service.yaml
```

Check the Service:

```bash
kubectl get services
```

Example:

```text
NAME                 TYPE       CLUSTER-IP      PORT(S)
notes-api-service    NodePort   10.x.x.x        80:30xxx/TCP
```

---

# 10. Access the Application

The easiest way with Minikube is:

```bash
minikube service notes-api-service
```

Minikube will provide the URL.

You can also get the Service URL:

```bash
minikube service notes-api-service --url
```

Example:

```text
http://192.168.49.2:30080
```

---

# 11. Test the API

## Test the root endpoint

Using curl:

```bash
curl http://<SERVICE_URL>/
```

Example:

```bash
curl http://192.168.49.2:30080/
```

---

## Test the health endpoint

```bash
curl http://<SERVICE_URL>/health
```

Expected response:

```json
{
    "status": "healthy"
}
```

This endpoint is also used by Kubernetes health probes.

---

## Get all notes

```bash
curl http://<SERVICE_URL>/notes
```

Or using Postman:

```text
GET http://<SERVICE_URL>/notes
```

---

## Create a note

Using curl:

```bash
curl -X POST http://<SERVICE_URL>/notes \
-H "Content-Type: application/json" \
-d '{"title":"My first note","content":"Hello Kubernetes"}'
```

Or in Postman:

```text
POST http://<SERVICE_URL>/notes
```

Select:

```text
Body
→ raw
→ JSON
```

and use:

```json
{
    "title": "My first note",
    "content": "Hello Kubernetes"
}
```

---

## Get a specific note

If the note ID is `1`:

```bash
curl http://<SERVICE_URL>/notes/1
```

Or:

```text
GET http://<SERVICE_URL>/notes/1
```

---

# 12. Verify Kubernetes Resources

Check all resources:

```bash
kubectl get all
```

Check Pods:

```bash
kubectl get pods
```

Check Deployments:

```bash
kubectl get deployments
```

Check ReplicaSets:

```bash
kubectl get replicasets
```

Check Services:

```bash
kubectl get services
```

Check HPA:

```bash
kubectl get hpa
```

---

# 13. Horizontal Pod Autoscaler

The application is configured with:

```text
Minimum replicas: 2
Maximum replicas: 6
```

Apply the HPA:

```bash
kubectl apply -f k8s/hpa.yaml
```

Check the HPA:

```bash
kubectl get hpa
```

For detailed information:

```bash
kubectl describe hpa notes-api-hpa
```

Watch the HPA:

```bash
kubectl get hpa -w
```

Watch Pods at the same time:

```bash
kubectl get pods -w
```

---

# 14. Test Kubernetes Self-Healing

The Deployment maintains the desired number of Pods.

Check the Pods:

```bash
kubectl get pods
```

Delete one:

```bash
kubectl delete pod <pod-name>
```

Immediately watch the Pods:

```bash
kubectl get pods -w
```

Kubernetes should automatically create a replacement Pod.

This demonstrates Kubernetes self-healing.

---

# 15. Test Rolling Updates

Build a new version of the Docker image:

```bash
docker build -t <DOCKERHUB_USERNAME>/k8s-notes-api:v2 .
```

Push it:

```bash
docker push <DOCKERHUB_USERNAME>/k8s-notes-api:v2
```

Update the Deployment image:

```bash
kubectl set image deployment/notes-api \
notes-api=<DOCKERHUB_USERNAME>/k8s-notes-api:v2
```

Watch the rollout:

```bash
kubectl rollout status deployment/notes-api
```

Watch the Pods:

```bash
kubectl get pods -w
```

Check rollout history:

```bash
kubectl rollout history deployment/notes-api
```

---

# 16. Roll Back a Deployment

If the new version has a problem:

```bash
kubectl rollout undo deployment/notes-api
```

Check the rollout:

```bash
kubectl rollout status deployment/notes-api
```

---

# 17. CronJob

The project includes a Kubernetes CronJob that runs every minute.

Apply it:

```bash
kubectl apply -f k8s/cronjob.yaml
```

Check the CronJob:

```bash
kubectl get cronjobs
```

Check Jobs created by the CronJob:

```bash
kubectl get jobs
```

Check CronJob Pods:

```bash
kubectl get pods
```

View the logs:

```bash
kubectl logs <cronjob-pod-name>
```

Expected output:

```text
Backup completed
```

or:

```text
Backup completed: 2026-09-15 12:00:00
```

---

# 18. Health Probes

The Deployment uses:

* Liveness probe
* Readiness probe

Both check:

```text
/health
```

View the configured probes:

```bash
kubectl describe deployment notes-api
```

You can also inspect an individual Pod:

```bash
kubectl describe pod <pod-name>
```

Look for:

```text
Liveness:
Readiness:
```

---

# 19. Troubleshooting

## Check Pod status

```bash
kubectl get pods
```

---

## Check Pod details

```bash
kubectl describe pod <pod-name>
```

---

## Check application logs

```bash
kubectl logs <pod-name>
```

---

## Follow logs in real time

```bash
kubectl logs -f <pod-name>
```

---

## Check Deployment

```bash
kubectl describe deployment notes-api
```

---

## Check ReplicaSet

```bash
kubectl get replicasets
kubectl describe replicaset <replicaset-name>
```

---

## Check Service

```bash
kubectl get svc
kubectl describe svc notes-api-service
```

---

## Check Service endpoints

```bash
kubectl get endpoints notes-api-service
```

The endpoints should contain the IP addresses of the application Pods.

---

## Test the application from inside a Pod

```bash
kubectl exec -it <pod-name> -- sh
```

Then:

```bash
curl http://localhost:5000/health
```

---

## Check events

```bash
kubectl get events --sort-by=.lastTimestamp
```

This is useful when Pods fail to start or images cannot be pulled.

---

# 20. Useful kubectl Commands

### Watch Pods

```bash
kubectl get pods -w
```

### Get everything

```bash
kubectl get all
```

### Delete the application

```bash
kubectl delete -f k8s/
```

### Restart the Deployment

```bash
kubectl rollout restart deployment notes-api
```

### Check rollout status

```bash
kubectl rollout status deployment/notes-api
```

### Scale manually

```bash
kubectl scale deployment notes-api --replicas=5
```

Check:

```bash
kubectl get pods
```

> If an HPA is configured, the HPA controls the desired replica count based on its scaling policy, so manual scaling may be overridden.

---

# 21. Complete Deployment

After cloning the repository, the basic deployment process is:

```bash
minikube start

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/cronjob.yaml
```

Verify everything:

```bash
kubectl get all
```

Check Pods:

```bash
kubectl get pods
```

Check HPA:

```bash
kubectl get hpa
```

Get the application URL:

```bash
minikube service notes-api-service --url
```

Test:

```bash
curl <SERVICE_URL>/health
```

---

# 22. Cleanup

To remove the Kubernetes resources:

```bash
kubectl delete -f k8s/
```

Stop Minikube:

```bash
minikube stop
```

Delete the Minikube cluster completely:

```bash
minikube delete
```

---

# What I Learned

Through this project I practiced:

* Building and packaging a Flask application with Docker
* Publishing Docker images to Docker Hub
* Deploying containers using Kubernetes
* Managing application replicas with Deployments
* Understanding ReplicaSets
* Exposing applications using Kubernetes Services
* Configuring applications using ConfigMaps
* Managing sensitive configuration using Secrets
* Configuring CPU-based Horizontal Pod Autoscaling
* Creating scheduled Kubernetes CronJobs
* Implementing liveness and readiness probes
* Testing Kubernetes self-healing
* Performing rolling updates
* Rolling back failed deployments
* Troubleshooting Kubernetes resources using `kubectl`

---

# Future Improvements

Possible improvements for the project:

* Add Kubernetes Ingress
* Add persistent storage using PersistentVolumes
* Add Metrics Server
* Add Prometheus and Grafana monitoring
* Add CI/CD with GitHub Actions
* Add automated Docker image builds
* Add automated Kubernetes deployment
* Add a database such as PostgreSQL
* Add TLS/HTTPS
* Add authentication and authorization
* Add automated API tests
* Deploy to AWS EKS

---

# Project Status

**Completed**

The application is containerized with Docker and deployed to Kubernetes with:

* 3 initial replicas
* Kubernetes Deployment
* ReplicaSet
* NodePort Service
* Horizontal Pod Autoscaler
* ConfigMap
* Secret
* CronJob
* Liveness probe
* Readiness probe
* Docker Hub image

---

## Author

**Saif Kbishi**

This project was created as part of my hands-on DevOps and Kubernetes learning journey.


