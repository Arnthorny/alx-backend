import express from "express";
import redis from "redis";
import { promisify } from "util";

const client = redis
  .createClient()
  .on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err}`)
  );
client.on("ready", () => console.log("Redis client connected to the server"));
const app = express();

const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

function getItemById(id) {
  const prod = listProducts.find((prod) => prod.itemId === id);
  return prod !== undefined ? { ...prod } : undefined;
}

function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock, redis.print);
}

async function getCurrentReservedStockById(itemId) {
  const getFunc = promisify(client.get).bind(client);
  const reserveStock = await getFunc(`item.${itemId}`);

  return reserveStock;
}

app.get("/list_products", (req, res) => {
  res.json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  const errReply = { status: "Product not found" };
  const item = getItemById(Number.parseInt(req.params.itemId));
  if (item === undefined) res.json(errReply);
  else {
    await getCurrentReservedStockById(req.params.itemId).then((stockRes) => {
      const stock = stockRes ? Number.parseInt(stockRes) : 0;
      item.currentQuantity = item.initialAvailableQuantity - stock;
      res.json(item);
    });
  }
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(Number.parseInt(itemId));
  let stockLeft, stockReserved;
  if (item === undefined) res.json({ status: "Product not found" });
  else {
    await getCurrentReservedStockById(itemId).then((stockRes) => {
      stockReserved = stockRes ? Number.parseInt(stockRes) : 0;
      stockLeft = item.initialAvailableQuantity - stockReserved;
    });
    if (stockLeft < 1)
      res.json({ status: "Not enough stock available", itemId });
    else {
      reserveStockById(itemId, stockReserved + 1);
      res.json({ status: "Reservation confirmed", itemId });
    }
  }
});

const port = 1245;
const host = "0.0.0.0";

app.listen(port, host, () => {
  console.log(`Server is running on port ${port} on ${host}`);
});
