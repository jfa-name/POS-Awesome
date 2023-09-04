export function customSort(items) {
  const statuses = ['Unpaid', 'Partly Paid', 'Paid', /* Add other statuses here */];
  return items.sort((a, b) => {
    const statusA = statuses.indexOf(a.status);
    const statusB = statuses.indexOf(b.status);

    if (statusA === statusB) return 0;
    if (statusA === -1) return -1;
    if (statusB === -1) return 1;

    return statusA - statusB;
  });
} 
