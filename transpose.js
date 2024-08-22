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

for (let i = 0; i < m; i++) {
  result.push([])
}

for (let i = 0; i < n; i++) {
  for (let j = 0; j < m; j++) {
    result[j][i] = values[i][j]
  }
}
console.log(result)

const map = input => {
  let result = '#input > '
  const map = {
    'MR-A 1.1': 'div1',
    'MR-A 1.2': 'div2',
    'MR-Till.v E 1.1': 'div13',
    'MR-Till.v E 1.2': 'div14'
  }
  return result += map[input] 
}

['MR-A 1.1', 'MR-Till.v E 1.2']
  .forEach(input => {
    console.log(input, '->', map(input))
  }
)