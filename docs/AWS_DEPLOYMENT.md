# AWS Deployment Guide

To deploy app to AWS you need to have:
- **Frontend**: S3 + CloudFront (CDN for static content)
- **Backend**: EC2 instance
- **Database**: RDS PostgreSQL

### The frontend app should be build and pushed to the S3 bucket and use CDN to serve static content 
The best option because is cheap and AWS manage whole traffic without our config.

### The backend app should be build using docker and pushed to the ECR (Elastic Container Registry) and run on the EC2 instance
It allows us to restart and run the same app version on the instance, it is easy to add Load Balancing in the future
if the traffic will increase, it is easy to scale the app. Very flexible architecture, can be changed to ECS or Kubernetes

### The database should be run on the RDS (Relational Database Service) instance
We don't have to manage postgres versions, we don't have to do updates manually, all maintenance is done by AWS.
It is easy to do snapshot and move e.g. to Aurora to scale database in the future