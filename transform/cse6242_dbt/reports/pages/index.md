---
title: Can you make money with Hurricanes?
---

<Details title='How to edit this page'>

  This page can be found in your project at `/pages/index.md`. Make a change to the markdown file and save it to see the change take effect in your browser.
</Details>

```sql categories
  select
      category
  from needful_things.orders
  group by category
```

<Dropdown data={categories} name=category value=category>
    <DropdownOption value="%" valueLabel="All Categories"/>
</Dropdown>

<Dropdown name=year>
    <DropdownOption value=% valueLabel="All Years"/>
    <DropdownOption value=2019/>
    <DropdownOption value=2020/>
    <DropdownOption value=2021/>
</Dropdown>

```sql orders_by_category
  select 
      date_trunc('month', order_datetime) as month,
      sum(sales) as sales_usd,
      category
  from needful_things.orders
  where category like '${inputs.category.value}'
  and date_part('year', order_datetime) like '${inputs.year.value}'
  group by all
  order by sales_usd desc
```

<BarChart
    data={orders_by_category}
    title="Sales by Month, {inputs.category.label}"
    x=month
    y=sales_usd
    series=category
/>

```sql stock_prices_all
  select
      *
  from analytics_marts.stock_prices
```

<LineChart
    data={stock_prices_all}
    title="Stock prices from 2014-2023"
    x=trading_date
    y={['adj_close_hd','adj_close_low','adj_close_spyx']} 
/>

```sql stock_prices_hurricane
  select
      *
  from analytics_marts.stock_prices
  WHERE EXTRACT(MONTH FROM trading_date) BETWEEN 6 AND 11
```

<LineChart
    data={stock_prices_hurricane}
    title="Stock prices during Hurricane Season 2014-2023"
    x=trading_date
    y={['adj_close_hd','adj_close_low','adj_close_spyx']} 
/>

## What's Next?
- [Connect your data sources](settings)
- Edit/add markdown files in the `pages` folder
- Deploy your project with [Evidence Cloud](https://evidence.dev/cloud)

## Get Support
- Message us on [Slack](https://slack.evidence.dev/)
- Read the [Docs](https://docs.evidence.dev/)
- Open an issue on [Github](https://github.com/evidence-dev/evidence)
