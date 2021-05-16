for i in {2..200};
 do convert out1.png out$i.png -evaluate-sequence xor xor$i.png;
done
