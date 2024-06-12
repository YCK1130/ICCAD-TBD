/* Generated by Yosys 0.9 (git sha1 1979e0b) */

module top_809960632_810038711_1598227639_893650103(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n27, n53, n55, n69, n78, n75, n82_inv, n80_inv);
  wire _000_;
  wire _001_;
  wire _002_;
  wire _003_;
  wire _004_;
  wire _005_;
  wire _006_;
  wire _007_;
  wire _008_;
  wire _009_;
  wire _010_;
  wire _011_;
  wire _012_;
  wire _013_;
  wire _014_;
  wire _015_;
  wire _016_;
  wire _017_;
  wire _018_;
  wire _019_;
  wire _020_;
  wire _021_;
  wire _022_;
  wire _023_;
  wire _024_;
  wire _025_;
  wire _026_;
  wire _027_;
  wire _028_;
  wire _029_;
  wire _030_;
  wire _031_;
  wire _032_;
  wire _033_;
  wire _034_;
  wire _035_;
  wire _036_;
  wire _037_;
  wire _038_;
  wire _039_;
  wire _040_;
  wire _041_;
  wire _042_;
  wire _043_;
  wire _044_;
  wire _045_;
  wire _046_;
  wire _047_;
  wire _048_;
  wire _049_;
  wire _050_;
  wire _051_;
  wire _052_;
  wire _053_;
  wire _054_;
  wire _055_;
  wire _056_;
  wire _057_;
  wire _058_;
  wire _059_;
  wire _060_;
  wire _061_;
  wire _062_;
  input n1;
  input n10;
  input n11;
  input n12;
  input n13;
  input n14;
  input n2;
  output n27;
  input n3;
  input n4;
  input n5;
  output n53;
  output n55;
  input n6;
  output n69;
  input n7;
  output n75;
  output n78;
  input n8;
  output n80_inv;
  output n82_inv;
  input n9;
  nor_5 _063_ (
    .A(n7),
    .B(n12),
    .Y(_030_)
  );
  nor_5 _064_ (
    .A(n11),
    .B(_000_),
    .Y(_031_)
  );
  nor_5 _065_ (
    .A(_030_),
    .B(_031_),
    .Y(_032_)
  );
  or_6 _066_ (
    .A(n1),
    .B(_032_),
    .Y(_033_)
  );
  nor_5 _067_ (
    .A(n12),
    .B(n3),
    .Y(_034_)
  );
  nor_5 _068_ (
    .A(n11),
    .B(_002_),
    .Y(_035_)
  );
  nor_5 _069_ (
    .A(_034_),
    .B(_035_),
    .Y(_036_)
  );
  nor_5 _070_ (
    .A(n6),
    .B(_036_),
    .Y(_037_)
  );
  nand_5 _071_ (
    .A(_022_),
    .B(_037_),
    .Y(_038_)
  );
  nand_5 _072_ (
    .A(_033_),
    .B(_038_),
    .Y(_039_)
  );
  nor_5 _073_ (
    .A(_029_),
    .B(_039_),
    .Y(n69)
  );
  and_6 _074_ (
    .A(_022_),
    .B(_033_),
    .Y(_040_)
  );
  nand_5 _075_ (
    .A(n2),
    .B(_003_),
    .Y(_041_)
  );
  nor_5 _076_ (
    .A(n10),
    .B(n14),
    .Y(_042_)
  );
  nand_5 _077_ (
    .A(n10),
    .B(_005_),
    .Y(_043_)
  );
  nand_5 _078_ (
    .A(n5),
    .B(_043_),
    .Y(_044_)
  );
  nor_5 _079_ (
    .A(_042_),
    .B(_044_),
    .Y(_045_)
  );
  nor_5 _080_ (
    .A(_013_),
    .B(_045_),
    .Y(_046_)
  );
  nand_5 _081_ (
    .A(_041_),
    .B(_046_),
    .Y(_047_)
  );
  nor_5 _082_ (
    .A(n8),
    .B(_045_),
    .Y(_048_)
  );
  nand_5 _083_ (
    .A(_047_),
    .B(_048_),
    .Y(_049_)
  );
  nor_5 _084_ (
    .A(_009_),
    .B(_018_),
    .Y(_050_)
  );
  nand_5 _085_ (
    .A(_049_),
    .B(_050_),
    .Y(_051_)
  );
  nor_5 _086_ (
    .A(n8),
    .B(_018_),
    .Y(_052_)
  );
  nand_5 _087_ (
    .A(_051_),
    .B(_052_),
    .Y(_053_)
  );
  nor_5 _088_ (
    .A(_026_),
    .B(_037_),
    .Y(_054_)
  );
  nand_5 _089_ (
    .A(_053_),
    .B(_054_),
    .Y(_055_)
  );
  nor_5 _090_ (
    .A(n8),
    .B(_026_),
    .Y(_056_)
  );
  nand_5 _091_ (
    .A(_055_),
    .B(_056_),
    .Y(_057_)
  );
  xnor_4 _092_ (
    .A(_040_),
    .B(_057_),
    .Y(_058_)
  );
  not_8 _093_ (
    .A(_058_),
    .Y(n75)
  );
  xor_4 _094_ (
    .A(_053_),
    .B(_054_),
    .Y(n53)
  );
  xor_4 _095_ (
    .A(_041_),
    .B(_046_),
    .Y(n27)
  );
  xor_4 _096_ (
    .A(_049_),
    .B(_050_),
    .Y(n55)
  );
  and_6 _097_ (
    .A(n27),
    .B(n55),
    .Y(_059_)
  );
  nand_5 _098_ (
    .A(n53),
    .B(_059_),
    .Y(_060_)
  );
  nor_5 _099_ (
    .A(_058_),
    .B(_060_),
    .Y(n78)
  );
  nor_5 _100_ (
    .A(_028_),
    .B(_045_),
    .Y(_061_)
  );
  not_8 _101_ (
    .A(_061_),
    .Y(n80_inv)
  );
  nand_5 _102_ (
    .A(n2),
    .B(_061_),
    .Y(_062_)
  );
  nand_5 _103_ (
    .A(n69),
    .B(_062_),
    .Y(n82_inv)
  );
  not_8 _104_ (
    .A(n7),
    .Y(_000_)
  );
  not_8 _105_ (
    .A(n4),
    .Y(_001_)
  );
  not_8 _106_ (
    .A(n3),
    .Y(_002_)
  );
  not_8 _107_ (
    .A(n8),
    .Y(_003_)
  );
  not_8 _108_ (
    .A(n10),
    .Y(_004_)
  );
  not_8 _109_ (
    .A(n13),
    .Y(_005_)
  );
  nor_5 _110_ (
    .A(n12),
    .B(n4),
    .Y(_006_)
  );
  nor_5 _111_ (
    .A(n11),
    .B(_001_),
    .Y(_007_)
  );
  nor_5 _112_ (
    .A(_006_),
    .B(_007_),
    .Y(_008_)
  );
  nor_5 _113_ (
    .A(n9),
    .B(_008_),
    .Y(_009_)
  );
  nor_5 _114_ (
    .A(n12),
    .B(n10),
    .Y(_010_)
  );
  nor_5 _115_ (
    .A(n11),
    .B(_004_),
    .Y(_011_)
  );
  nor_5 _116_ (
    .A(_010_),
    .B(_011_),
    .Y(_012_)
  );
  nor_5 _117_ (
    .A(n5),
    .B(_012_),
    .Y(_013_)
  );
  nor_5 _118_ (
    .A(_009_),
    .B(_013_),
    .Y(_014_)
  );
  nor_5 _119_ (
    .A(n4),
    .B(n14),
    .Y(_015_)
  );
  nand_5 _120_ (
    .A(n4),
    .B(_005_),
    .Y(_016_)
  );
  nand_5 _121_ (
    .A(n9),
    .B(_016_),
    .Y(_017_)
  );
  nor_5 _122_ (
    .A(_015_),
    .B(_017_),
    .Y(_018_)
  );
  nand_5 _123_ (
    .A(n7),
    .B(n13),
    .Y(_019_)
  );
  nand_5 _124_ (
    .A(_000_),
    .B(n14),
    .Y(_020_)
  );
  nand_5 _125_ (
    .A(_019_),
    .B(_020_),
    .Y(_021_)
  );
  nand_5 _126_ (
    .A(n1),
    .B(_021_),
    .Y(_022_)
  );
  nor_5 _127_ (
    .A(n3),
    .B(n14),
    .Y(_023_)
  );
  nand_5 _128_ (
    .A(n3),
    .B(_005_),
    .Y(_024_)
  );
  nand_5 _129_ (
    .A(n6),
    .B(_024_),
    .Y(_025_)
  );
  nor_5 _130_ (
    .A(_023_),
    .B(_025_),
    .Y(_026_)
  );
  nor_5 _131_ (
    .A(_018_),
    .B(_026_),
    .Y(_027_)
  );
  nand_5 _132_ (
    .A(_022_),
    .B(_027_),
    .Y(_028_)
  );
  nor_5 _133_ (
    .A(_014_),
    .B(_028_),
    .Y(_029_)
  );
endmodule
