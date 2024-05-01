Introduction
------------
* Advances in tools, cloud and infrastructure are making it possible to do "microservices first" approach.
  - It may be easier than starting using a monolith and then refactoring.

* Microservices add complexity in the areas of:
  - Infrastructure
    * There's more of it (message busses, databases, application servers, etc.)
  - Integration
    * To test a single feature we sometimes have to span multiple services

* Any complexity added by microservices must be offset by their benefits.
  - This should be a decision made project by project basis.

* A large microservices system can become far too complex for a single person to understand as a whole,
  however, it's built out of small parts that on their own should be manageable.

* Microservice
  - Has its own deployment schedule
  - Usually has its own storage solution or a partition in a shared storage solution
  - has a way to communicate with other services
  - On its own not very useful, but in a system makes more sense

* Monolith
  - Requires an entire deployment even if only a small module in it needs an update.
    * This introduces higher risk for updating the system
  - Harder to test 
  - Easier to start off and integrate

* To successfully develop a microservices system, we need:
  - Automation 
  - Testing
  - Understanding of distributed systems
  - Diverse skillset (multiple different technologies)