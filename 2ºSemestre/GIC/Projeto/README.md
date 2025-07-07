# Project for the class of Computer Infrastructure Management 2024/25

This project focuses on the construction, management and operation of a product supported by a multi-component stack, on a kubernetes cluster. The goal is to design, implement, and operate a resilient, reliable, highly available, and observable system, leveraging standard kubernetes mechanisms. It should be noticed that the stack should mostly rely on existing, open source, software, with additional hooks and features added solely for the purpose of fulfilling the requirements of this project.

The objective of this project is to design and implement a simplified multitiered e-commerce platform serving products at a global scale. You may choose which products you will be providing. The following components must be considered:

- **Frontend:** a web application based on a existing CMS or similar platform, which will be accessed by users when they which to acquire your products. If this is integrated with the backend, consider this as the front facing components, and especially the static components of your application.

- **Backend:** the application handling requests from the frontend, and doing some processing.
- **Database:** A relational database for persistent storage
- **Cache:** A caching layer to allow distributed operation of the components
- **Content Delivery Network:** A system providing static contents to users in optimal ways.
- **Monitoring system:** a system that can be used to analyze and forecast system operation, hardware requirements, and user behavior

## Project Requirements

The deployed system must fulfill the following criteria:

- **Resilient:** system should be able to recover from errors, such as software crashes and API failures, having the required methods to prevent excessive use of resources and to detect the state of the different components

- **Reliable:** system should operate in a consistent manner, without frequent or occasional errors

- **Highly Available:** system must be able to follow user demand and minimize downtime

- **Observable:** system must provide adequate information allowing to measure the operation of the different components, and key user behavior. This should also allow to pinpoint errors to the near past.

- **Automated:** the entire deployment must be automated through a single shell script, and there should be a process to update the individual components.

- **Secure:** there should be segmentation of the different components and the correct use of configurations and secrets.

- **Documented:** there should be documentation regarding the product, design solutions, as well as evidences of the correct fulfillment of the previous criteria.

---

## Grades

| Delivery | Grade |
| :------: | :---: |
| Product Presentation | 17 |
| 1st Report | 16 |
| 2nd Report | 17 |

---

## Our Solution — ByteBazaar

**ByteBazaar** is an e-commerce platform for technological products, based on and adapted from the open-source project [alimhtsai/E_commerce](https://github.com/alimhtsai/E_commerce). We restructured, containerized, and extended the architecture to support Kubernetes-native operation and academic requirements.

It includes:

- A web admin panel written in **Angular**, served via **NGINX**
- A backend developed in **.NET 8**, composed of:
    - `REST API`: for handling client requests
    - `Infrastructure`: database/cache access
    - `Core`: domain logic and models
- A relational database (**MySQL**) to store persistent data
- A caching database (**Redis**) with **Sentinel** for high availability
- An **Upload Server** (Node.js) to allow image uploads from the frontend
- A **CDN**, externally hosted by the department at `http://cdn.deti/bytebazaar`
- A **Budibase** instance for internal content and form management
- An observability layer with:
    - **Prometheus** for metrics
    - **Grafana** for dashboards
    - **Jaeger** for distributed tracing
    - **Otel Collector** for metric aggregation and export

---

## Deployment Architecture

![Deployment Architecture for ByteBazaar](/images/ByteBazaar_Architecture.jpg)

---

## Accessing the Deployed Application

To access the platform deployed on the Kubernetes cluster:

1. Connect to the **eduroam** network;
2. Add the following line to your `/etc/hosts`:

```bash
193.136.82.35   bytebazaar.k3s api.bytebazaar.k3s cdn.deti bytebazaar.k3s grafana.bytebazaar.k3s otel.bytebazaar.k3s admin.bytebazaar.k3s
```

3. Use the following services:

| Service         | URL                                |
|-----------------|-------------------------------------|
| Web Application     | https://bytebazaar.k3s/              |
| API (Backend)   | https://api.bytebazaar.k3s/          |
| CDN             | https://cdn.deti/bytebazaar/         |
| Admin UI        | http://admin.bytebazaar.k3s/app/bytebazaar       |
| Grafana         | http://grafana.bytebazaar.k3s/      |
| Otel Collector | https://otel.bytebazaar.k3s/             |

**Budibase credentials:**

```
Email: admin@admin.com
Password: admin123456789
```

---

## Deliverables

- The product presentation can be found in this location [./reports/GIC_product_presentation.pdf](./reports/GIC_product_presentation.pdf)
- The report for the first delivery can be found in this location [./reports/GIC_1st_report.pdf](./reports/GIC_1st_report.pdf)
- The report for the second and final delivery can be found in this location [./reports/Final_Report_GIC.pdf](./reports/Final_Report_GIC.pdf)
- A demo presentation of the final solution can be found [here](./demo-gic-bytebazaar.mp4)

---

## Project Structure

```bash
.
├── E_commerce               
├── k3s                     
│   ├── backend/
│   ├── client/
│   ├── cdn/
│   ├── redis/
│   ├── mysql/
│   ├── budibase/
│   ├── upload-server/
│   ├── observability/
│   ├── ingress/
│   └── scripts/
├── docs               
└── README.md
```

---

## Authors

<table>
    <tr>
        <td align="center" width="50px;"></td>
            <td align="center"><a href="https://github.com/caridade1706"><img src="https://avatars.githubusercontent.com/u/113480231?v=4" width="150px;" alt="Caridade"/><br /><sub><b>Tiago Gomes</b><br><i>108307</i></sub></a><hr><a href="https://github.com/caridade1706" title="Code">💻</a> <a href="https://github.com/caridade1706" title="Tools">🔀</a> <a href="https://github.com/caridade1706" title="Tools">🔨</a></td>
            <td align="center"><a href="https://github.com/RobertoCastro391"><img src="https://avatars.githubusercontent.com/u/115174164?v=4" width="150px;" alt="Roberto"/><br /><sub><b>Roberto Castro</b><br><i>107133</i></sub></a><hr><a href="https://github.com/RobertoCastro391" title="Code">💻</a><a href="https://github.com/RobertoCastro391 title="Tools">🔀</a><a href="https://github.com/RobertoCastro391" title="Tools">🔨</a></td>
            <td align="center"><a href="https://github.com/zegameiro"><img src="https://avatars0.githubusercontent.com/zegameiro?v=3" width="150px;" alt="Gameiro"/><br /><sub><b>José Gameiro</b><br><i>108840</i></sub></a><hr><a href="https://github.com/zegameiro" title="Code">💻</a><a href="https://github.com/zegameiro" title="Tools">🔀</a><a href="https://github.com/zegameiro" title="Tools">🔨</a></td>
        <td align="center" width="50px;"></td>
    </tr>
</table>