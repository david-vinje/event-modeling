const hashes = [
  {
    Key: 'A',
    Value: 'a, b, c, d'
  },
  {
    Key: 'B',
    Value: '1, 2, 3, 4'
  },
  {
    Key: 'C',
    Value: 'x, y, z, w'
  }
]

const values = hashes.map(obj => {
  return obj.Value.split(', ')
})

const n = values.length
const m = values[0].length
const result = []

for (let i=0; i<m; i++) {
  result.push([])
}

for (let i=0; i<n; i++) {
  for (let j=0; j<m; j++) {
    result[j][i] = values[i][j]
  }
}

console.log(result)