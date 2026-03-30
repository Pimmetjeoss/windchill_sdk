# Querying with the DateTimeOffset Property


Windchill REST Services enables DateTimeOffset property to be used in $filter expressions. Windchill enables DateTimeOffset properties to be persisted in the database. However, it only allows the date portion of the DateTimeOffset property to be used in queries. Windchill stores all the DateTimeOffset properties in UTC format.

When you query with DateTimeOffset property in $filter expressions, you must specify both the date and time in UTC format. Windchill REST Services returns an error if the date and time properties in $filter expressions are specified in any other time zone. The $filter expressions with a DateTimeOffset property are evaluated only on the date portion of the property. For example, if you specify the expression $filter=CreatedOn eq 2018-01-20T01:52:16Z, the service qualifies all the entities created on January 20, 2018, in the UTC time zone regardless of the time specified in the expression.

For example, the URL used in $filter expression with DateTimeOffset property is:

https://windchill.ptc.com/Windchill/servet/odata/ProdMgmt/Parts?$filter=CreatedOn eq 2018-01-20T00:00:00Z
