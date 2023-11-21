<<<<<<< HEAD
<<<<<<< HEAD
# AuthMS
=======
# DockerDemo
>>>>>>> f20191b (Initial commit)
=======
# DockerDemo

## Introduction

This project is a simple FastAPI application running on a Kubernetes cluster. The application is packaged in a Docker container and deployed using Kubernetes. The application exposes a single endpoint, `/hello/{name}`, which returns a greeting message.

## Installation

### Prerequisites

Before you can run this project, you need to have the following tools installed on your machine:

- Docker: Docker is used to build and run the application container. You can follow the official Docker installation guide for your operating system [Source 3](https://www.jetbrains.com/guide/python/tutorials/fastapi-aws-kubernetes/kubernetes_deploy/).
- Minikube: Minikube is a tool that runs a single-node Kubernetes cluster in a virtual machine on your machine. You can follow the official Minikube installation guide for your operating system [Source 8](https://linuxiac.com/how-to-install-minikube-on-linux/).
- kubectl: kubectl is a command-line tool for controlling Kubernetes clusters. You can follow the official kubectl installation guide for your operating system [Source 2](https://kubernetes.io/docs/setup/minikube/).
- PyCharm: PyCharm is an integrated development environment (IDE) for Python. You can download PyCharm from the official JetBrains website.
- Kubernetes Plugin for PyCharm: This plugin provides support for Kubernetes in PyCharm. You can install it from the JetBrains plugin marketplace in PyCharm.

### Building and Running the Application
```<username>``` is referring to your dockerhub username.
1. Build the Docker image:

   ```bash
   docker build -t <username>/fastapi-demo:latest .
   ```

2. Push the Docker image to a Docker registry. If you don't have a Docker registry, you can use Docker Hub. Replace `<username>` with your Docker Hub username:

   ```bash
   docker push <username>/fastapi-demo:latest
   ```

3. Start Minikube:

   ```bash
   minikube start
   ```

4. Deploy the application to Minikube:

   ```bash
   kubectl apply -f k8s/
   ```

5. Check the status of the application:

   ```bash
   kubectl get pods
   ```

### Accessing the Application

The application is exposed on a NodePort service. You can access the application at `localhost:30010`. If you want to access the application at `localhost:8000`, you can use `kubectl port-forward` to forward a local port to a port on the pod:

```bash
kubectl port-forward pod/<pod-name> 8000:8000 -n fastapi-demo
```

Replace `<pod-name>` with the name of your pod.

## Configuration

The application is configured to run on port 8000 inside the Docker container. The Dockerfile specifies the command to start the application:

```Dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The Kubernetes service is configured to expose port 5000 on the container and map it to port 8000 on the node. This is specified in the `service.yml` file:

```yaml
apiVersion: v1
kind: Service
metadata:
 name: fastapi-demo
spec:
 selector:
   app: fastapi-deployment
 ports:
   - protocol: TCP
     port: 5000
     targetPort: 8000
 type: NodePort
```

The `targetPort` is set to 8000, which is the port your application is running on. The `port` is the port that the service will expose, which is 5000 in this case. The `type` is set to `NodePort`, which means that the service will be accessible on a static port on each Node in your cluster.

## Tests

The tests for this application are written using FastAPI's test client and Python's built-in unittest module. The test client allows you to make requests to your application and check the responses.

### Running the Tests

To run the tests, you will need to have Python and the necessary dependencies installed on your machine. If you have not done so already, you can install the dependencies using pip and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Once the dependencies are installed, you can run the tests using the following command:

```bash
python -m unittest discover -s tests
```

This command will discover and run all tests in the `tests` directory.


## Conclusion

This project demonstrates how to package a FastAPI application in a Docker container and deploy it on a Kubernetes cluster. It also shows how to access the application from your local machine.
<<<<<<< HEAD
>>>>>>> 5385609 (Update README file)
=======
>>>>>>> 92cc113 (Add App Tests)
