package main

import {
  "os"
}

type transition struct {
  M int
  N int
  inputs [M]chan int //M input channels, cannot be 0
  outputs [N]chan int //N output channels, cannot be 0
}

//make M input channels (buffer size 1) & N output channels (buffer size 1)
func New(M int, N int) {
  var inputs [M]chan int
  for i := range inputs {
     inputs[i] = make(chan int, 1)
  }

  var outputs [N]chan int
  for j := range outputs {
     outputs[i] = make(chan int, 1)
  }

  t = transition {M, N, inputs, outputs}
  return t
}

//check if all M inputs are full
func (t transition) Eligible() {
  eligible := true
  for i := range t.inputs {
    if len(t.inputs[i]) != cap(t.inputs[i]){  //if any input channel is not full, transition is not eligible to fire
      eligible = false
    }
  }
  return eligible
}

//consume 1 token from each input & produce 1 token to each output
func (t transition) Fire() {
  for i := range t.inputs {
    <- t.inputs[i]
  }

  token := 1  //token = int with value 1
  for j := range t.outputs {
    t.outputs[i] <- token
  }
}

func (t transition) Run() {
  for {
    if t.Eligible(){
      t.Fire()
    }
  }
}
