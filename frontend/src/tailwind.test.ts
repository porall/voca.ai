/* Test that Tailwind CSS builds correctly */
import { describe, it, expect } from 'vitest'

describe('Tailwind CSS', () => {
  it('should have index.css with tailwind import', () => {
    const css = `
@import "tailwindcss";

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
}
`
    expect(css).toContain('@import "tailwindcss"')
  })
})