export const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000);

  const day = String(date.getUTCDate()).padStart(2, "0");
  const month = String(date.getUTCMonth() + 1).padStart(2, "0"); // Months are 0-indexed
  const year = date.getUTCFullYear();

  return `${year}-${month}-${day}`;
};
