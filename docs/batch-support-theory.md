# Processing Batch Requests


Using batch requests, you can group multiple operations in a single HTTP request. Use the $batch attribute to request data and perform operations on the data.

For example, run the batch request as below:

https://windchill.ptc.com/Windchill/servlet/odata/<domain>/$batch

In a batch request, you can specify a series of individual batch requests or create change sets. Batch requests are represented as multipart MIME message. Specify the batch requests and change sets in relevant Content-Type header as distinct MIME parts. The requests are processed sequentially.

Individual batch requests support the following types of requests:

• Creating data

• Getting data

• Modifying data

• Invoking an action and function

If any of the individual batch requests from the series fail, the other batch requests are processed.

Change set is an atomic unit inside which you can define a set of requests. In a change set you define series of individual batch requests. However, if one or more individual batch requests from the series fail, the entire change set fails. In a change set, if the batch requests have modified any data before encountering a failed request, then all the data changes are rolled back. A change set has been implemented as a Windchill transaction.

Change set supports the following types of requests:

• Modifying data

• Invoking an action

Change sets do not support the GET operation.

After execution, batch requests return the appropriate HTTP response codes. The HTTP response body lists the response in the same order as the individual requests in the HTTP request body. However, the requests inside a change set may not be executed in the order specified in the change set.

From Windchill REST Services 1.3 onward, batch requests support references to entity and property values between requests and responses of different parts of a batch. A change set request can reference the property value of an entity from a change set of a previous batch request. To reference an entity property from the previous batch request, use the syntax $<Content-ID\_of\_changeset>/<property\_name>. In the following example, changeset2 references property Name from changeset1, which has Content-ID1\_1.

POST /ProdMgmt/$batch

Content-Type: multipart/mixed;boundary=batch

--batch

Content-Type: multipart/mixed;boundary=changeset1

--changeset1

Content-Type: application/http

Content-Transfer-Encoding:binary

Content-ID: 1\_1

POST ProdMgmt/Parts HTTP 1.1

Content-Type: application/json

{

... Part Entity Representation ...

}

--changeset1--

--batch

Content-Type: multipart/mixed;boundary=changeset2

--changeset2

Content-Type: application/http

Content-Transfer-Encoding:binary

Content-ID: 2\_1

POST DocMgmt/Documents HTTP 1.1

Content-Type: application/json

{

...

"Name": $1\_1/Name,

...

}

--changeset2--

--batch--
