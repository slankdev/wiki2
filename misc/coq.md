
# Coq

```
Fixpoint fact (n : nat) : nat :=
  match n with
  | O => 1
  | S n0 => n * fact n0
  end.

Check fact.
Eval compute in 501 - 500.

Fixpoint my_larger0 (a : nat)(b : nat) : nat :=
  match a-b with
  | O => b
  | S _ => a
  end.

Eval compute in my_larger0 4 33333.

Fixpoint my_le (a b:nat) : bool :=
  match a with
  | O => true
  | S a0 =>
    match b with
    | O => false
    | S b0 => my_le a0 b0
    end
  end.

Fixpoint super_le (a b:nat) : bool :=
  match (a,b) with
  | (O, _) => true
  | (S _, O) => false
  | (S a0, S b0) => super_le a0 b0
  end.

Fixpoint my_larger (a b: nat) : nat :=
  match super_le a b with
  | true => b
  | false => a
  end.

Fixpoint super_larger (a b: nat) : nat :=
  if super_le a b then b else a.

Require Import Arith.
Require Import List.
Eval compute in 4::4::nil.

```
