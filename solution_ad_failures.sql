SELECT
    c.first_name || ' ' || c.last_name AS customer,
    COUNT(*) AS failures
FROM customers c
JOIN campaigns cp ON cp.customer_id = c.id
JOIN events e ON e.campaign_id = cp.id
WHERE e.status = 'failure'
GROUP BY c.id, c.first_name, c.last_name
HAVING COUNT(*) > 3
ORDER BY failures DESC, customer;
